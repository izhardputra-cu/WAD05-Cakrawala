import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator


class BarangBaru(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nama: str = Field(min_length=1, max_length=80)
    kategori: str = Field(min_length=1, max_length=40)
    jumlah_stok: int = Field(strict=True, ge=0)
    lokasi_gudang: str = Field(min_length=1, max_length=60)

    @field_validator("nama", "kategori", "lokasi_gudang")
    @classmethod
    def tidak_boleh_kosong(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Tidak boleh kosong")
        return value


class Barang(BarangBaru):
    id: int = Field(strict=True, gt=0)


app = FastAPI(
    title="Inventaris Kantor IRD",
    description="API untuk daftar barang inventaris kantor.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

seed_path = Path(__file__).with_name("seed_barang.json")
barang_db = [Barang.model_validate(item) for item in json.loads(seed_path.read_text(encoding="utf-8"))]
id_berikutnya = max((item.id for item in barang_db), default=0) + 1


@app.get(
    "/barang",
    response_model=list[Barang],
    tags=["Barang"],
    summary="Lihat semua barang",
    description="Mengambil seluruh barang inventaris, termasuk data awal dari seed JSON.",
)
def lihat_barang() -> list[Barang]:
    return barang_db


@app.post(
    "/barang",
    response_model=Barang,
    status_code=201,
    tags=["Barang"],
    summary="Tambah barang",
    description="Menambah barang baru dengan nama, kategori, jumlah stok, dan lokasi gudang.",
)
def tambah_barang(data: BarangBaru) -> Barang:
    global id_berikutnya
    barang = Barang(id=id_berikutnya, **data.model_dump())
    barang_db.append(barang)
    id_berikutnya += 1
    return barang


@app.delete(
    "/barang/{barang_id}",
    status_code=204,
    tags=["Barang"],
    summary="Hapus barang",
    description="Menghapus barang berdasarkan ID. ID yang tidak ada menghasilkan respons 404.",
)
def hapus_barang(barang_id: int) -> None:
    for index, barang in enumerate(barang_db):
        if barang.id == barang_id:
            barang_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
