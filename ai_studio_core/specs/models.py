from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from pydantic.config import ConfigDict
from pydantic.type_adapter import TypeAdapter


class AssetType(str, Enum):
    audio_sfx = "audio_sfx"
    music = "music"
    texture_2d = "texture_2d"
    sprite_2d = "sprite_2d"
    mesh_3d_hardsurface = "mesh_3d_hardsurface"
    character_3d_lowpoly = "character_3d_lowpoly"


class EngineTarget(str, Enum):
    godot = "godot"
    unity = "unity"
    unreal = "unreal"


class OutputFormat(str, Enum):
    png = "png"
    wav = "wav"
    ogg = "ogg"
    json = "json"
    glb = "glb"
    gltf = "gltf"
    xm = "xm"
    it = "it"


class OutputKind(str, Enum):
    primary = "primary"
    metadata = "metadata"
    preview = "preview"


class OutputSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: OutputKind
    format: OutputFormat
    path: str = Field(description="Relative path under the output root (no leading slash)")

    @field_validator("path")
    @classmethod
    def _validate_rel_path(cls, v: str) -> str:
        if not v or v.strip() != v:
            raise ValueError("path must be a non-empty string without leading/trailing whitespace")
        if "\\" in v:
            raise ValueError("path must use forward slashes ('/') only")
        if v.startswith(("/", "\\")):
            raise ValueError("path must be relative (no leading slash)")
        if ".." in v.split("/"):
            raise ValueError("path must not contain '..' segments")
        return v

    @model_validator(mode="after")
    def _ext_matches_format(self) -> "OutputSpec":
        expected_ext = "." + self.format.value
        if not self.path.lower().endswith(expected_ext):
            raise ValueError(f"path must end with '{expected_ext}' for format '{self.format.value}'")
        return self


class VariantSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    variant_id: str
    seed: int = Field(ge=0, le=2**32 - 1)


class BaseAssetSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(description="Stable identifier used in filenames and reports")
    asset_type: AssetType
    style_tags: list[str] = Field(default_factory=list)
    license: str
    seed: int = Field(ge=0, le=2**32 - 1)
    variants: list[VariantSpec] = Field(default_factory=list)
    outputs: list[OutputSpec] = Field(min_length=1)
    engine_targets: list[EngineTarget] | None = None
    description: str | None = None

    @field_validator("asset_id")
    @classmethod
    def _asset_id_format(cls, v: str) -> str:
        import re

        if not re.fullmatch(r"[a-z][a-z0-9_\\-]{2,63}", v):
            raise ValueError("asset_id must match [a-z][a-z0-9_-]{2,63}")
        return v

    @field_validator("style_tags")
    @classmethod
    def _style_tags_normalize(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for tag in v:
            if not isinstance(tag, str) or not tag.strip():
                raise ValueError("style_tags entries must be non-empty strings")
            out.append(tag.strip())
        return out

    @model_validator(mode="after")
    def _unique_output_paths(self) -> "BaseAssetSpec":
        paths = [o.path for o in self.outputs]
        if len(paths) != len(set(paths)):
            raise ValueError("outputs.path values must be unique")
        if not any(o.kind == OutputKind.primary for o in self.outputs):
            raise ValueError("outputs must include at least one entry with kind='primary'")
        return self


class AudioSfxSpec(BaseAssetSpec):
    asset_type: Literal[AssetType.audio_sfx]
    duration_seconds: float = Field(gt=0.01, le=30.0)
    sample_rate_hz: int = Field(ge=8000, le=96000)
    channels: int = Field(ge=1, le=2)

    @model_validator(mode="after")
    def _output_formats(self) -> "AudioSfxSpec":
        allowed = {OutputFormat.wav, OutputFormat.ogg}
        primary = [o for o in self.outputs if o.kind == OutputKind.primary]
        if any(o.format not in allowed for o in primary):
            raise ValueError("audio_sfx primary outputs must be wav or ogg")
        return self


class MusicSpec(BaseAssetSpec):
    asset_type: Literal[AssetType.music]
    tempo_bpm: int = Field(ge=40, le=260)
    loop: bool = True

    @model_validator(mode="after")
    def _output_formats(self) -> "MusicSpec":
        allowed = {OutputFormat.xm, OutputFormat.it}
        primary = [o for o in self.outputs if o.kind == OutputKind.primary]
        if any(o.format not in allowed for o in primary):
            raise ValueError("music primary outputs must be xm or it")
        return self


class TextureMapType(str, Enum):
    albedo = "albedo"
    normal = "normal"
    roughness = "roughness"
    metallic = "metallic"
    ao = "ao"
    emissive = "emissive"


class TextureMapSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    map_type: TextureMapType
    format: Literal[OutputFormat.png]


class Texture2DSpec(BaseAssetSpec):
    asset_type: Literal[AssetType.texture_2d]
    resolution: tuple[int, int] = Field(description="(width, height) in pixels")
    tileable: bool = True
    maps: list[TextureMapSpec] = Field(min_length=1)

    @field_validator("resolution")
    @classmethod
    def _resolution_constraints(cls, v: tuple[int, int]) -> tuple[int, int]:
        w, h = v
        if w <= 0 or h <= 0:
            raise ValueError("resolution values must be positive")
        if w > 8192 or h > 8192:
            raise ValueError("resolution too large (max 8192x8192)")
        return v

    @model_validator(mode="after")
    def _output_formats(self) -> "Texture2DSpec":
        primary = [o for o in self.outputs if o.kind == OutputKind.primary]
        if any(o.format != OutputFormat.png for o in primary):
            raise ValueError("texture_2d primary outputs must be png")
        return self


class PivotSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)


class Sprite2DSpec(BaseAssetSpec):
    asset_type: Literal[AssetType.sprite_2d]
    frame_width: int = Field(ge=1, le=2048)
    frame_height: int = Field(ge=1, le=2048)
    frame_count: int = Field(ge=1, le=4096)
    pivot: PivotSpec = Field(default_factory=lambda: PivotSpec(x=0.5, y=0.5))
    trim_transparent: bool = True

    @model_validator(mode="after")
    def _output_formats(self) -> "Sprite2DSpec":
        primary = [o for o in self.outputs if o.kind == OutputKind.primary]
        if any(o.format != OutputFormat.png for o in primary):
            raise ValueError("sprite_2d primary outputs must be png")
        return self


class GltfExportSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    format: Literal[OutputFormat.glb] = OutputFormat.glb
    require_uvs: bool = True
    require_normals: bool = True
    require_tangents: bool = False


class Mesh3DHardsurfaceSpec(BaseAssetSpec):
    asset_type: Literal[AssetType.mesh_3d_hardsurface]
    triangle_budget: int = Field(ge=12, le=200_000)
    max_material_slots: int = Field(ge=1, le=4, description="Hard cap to prevent combinatorial materials")
    use_normal_map: bool = True
    export: GltfExportSpec = Field(default_factory=GltfExportSpec)

    @model_validator(mode="after")
    def _tangents_when_normal_map(self) -> "Mesh3DHardsurfaceSpec":
        if self.use_normal_map and not self.export.require_tangents:
            raise ValueError("export.require_tangents must be true when use_normal_map is true")
        return self

    @model_validator(mode="after")
    def _output_formats(self) -> "Mesh3DHardsurfaceSpec":
        primary = [o for o in self.outputs if o.kind == OutputKind.primary]
        if any(o.format != OutputFormat.glb for o in primary):
            raise ValueError("mesh_3d_hardsurface primary outputs must be glb")
        return self


class SkeletonPreset(str, Enum):
    humanoid_basic_v1 = "humanoid_basic_v1"


class CharacterConstraints(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_bone_influences: int = Field(default=4, ge=1, le=4)
    max_bones: int = Field(default=64, ge=1, le=128)


class Character3DLowpolySpec(BaseAssetSpec):
    asset_type: Literal[AssetType.character_3d_lowpoly]
    triangle_budget: int = Field(ge=100, le=200_000)
    skeleton_preset: SkeletonPreset = SkeletonPreset.humanoid_basic_v1
    constraints: CharacterConstraints = Field(default_factory=CharacterConstraints)
    use_normal_map: bool = False
    export: GltfExportSpec = Field(default_factory=GltfExportSpec)

    @model_validator(mode="after")
    def _tangents_when_normal_map(self) -> "Character3DLowpolySpec":
        if self.use_normal_map and not self.export.require_tangents:
            raise ValueError("export.require_tangents must be true when use_normal_map is true")
        return self

    @model_validator(mode="after")
    def _output_formats(self) -> "Character3DLowpolySpec":
        primary = [o for o in self.outputs if o.kind == OutputKind.primary]
        if any(o.format != OutputFormat.glb for o in primary):
            raise ValueError("character_3d_lowpoly primary outputs must be glb")
        return self


AssetSpec = Annotated[
    Union[
        AudioSfxSpec,
        MusicSpec,
        Texture2DSpec,
        Sprite2DSpec,
        Mesh3DHardsurfaceSpec,
        Character3DLowpolySpec,
    ],
    Field(discriminator="asset_type"),
]

_asset_spec_adapter = TypeAdapter(AssetSpec)


def parse_asset_spec(data: dict) -> AssetSpec:
    return _asset_spec_adapter.validate_python(data)


def format_validation_error(e: ValidationError) -> str:
    lines: list[str] = ["Spec validation failed:"]
    for err in e.errors():
        loc = ".".join(str(p) for p in err.get("loc", [])) or "<root>"
        msg = err.get("msg", "invalid")
        lines.append(f"- {loc}: {msg}")
    return "\n".join(lines)
