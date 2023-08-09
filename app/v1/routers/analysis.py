from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.v1.schemas import simple as simple_schema
from app.utils import utils
from app.models import Url, Content
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()


@router.get('/prep')
async def prep():
    rtext = """Jakarta, CNN Indonesia -- Menteri Komunikasi dan Informatika (Menkominfo) Budi Arie Setiadi menyebut bakal mengatur kampanye partai politik di jagat maya yang melibatkan kecerdasan buatan alias AI. "Nanti kita kaji, kita atur yang baik," kata dia, di kantornya, Jakarta, Selasa (8/8). Pihaknya masih akan mengkaji secara komprehensif mengenai aturan pemilu terkait metode kampanye mana yang diperbolehkan di jagat maya. "Satu-satu dulu dong. Kita lihat mana yang secara regulasi diperbolehkan dan mana yang tidak diperbolehkan," tutur Budi, yang juga menjabat ketua umum kelompok relawan Pro Jokowi (Projo) itu. Sebelumnya, Ketua Badan Pemenangan Pemilu PPP Sandiaga Uno mengungkapkan punya strategi khusus di Pemilu 2024, di antaranya menyusun kampanye di jagat maya lewat pemanfaatan big data AI. "Kita juga sepakat bahwa target suara 11 juta ini akan kita jangkau dengan teknologi penggunaan social media, big data, dan artificial inteligence," kata Sandiaga dalam rapat Bappilu PPP. Deepfake Kepala Pusat Riset Kecerdasan Artificial dan Keamanan Siber di Badan Riset dan Inovasi Nasional (BRIN) Anto Satriyo Nugroho meminta masyarakat waspada terhadap penggunaan AI jelang Pemilu 2024. Pasalnya, sudah ada contoh penggunaan kecerdasan buatan untuk meniru suara tokoh politik tertentu dan menjadi sumber hoaks di Pemilu 2024. Hoaks itu memanfaatkan AI untuk menghasilkan deepfake yang merupakan gabungan dari istilah deep learning (pembelajaran mesin yang meniru cara otak manusia belajar, yakni mencontoh) dan fake (palsu). "Harus dicatat kita hanya mengandalkan suara atau video saja itu tidak cukup membuktikan suara itu asli atau tidak. Kita tidak bisa memakai itu untuk decision," kata Anto kepada CNNIndonesia.com beberapa waktu lalu. Penggunaan AI untuk dalam konteks kepentingan politik sudah ditunjukkan Partai Republik AS. Pada April, Komite Partai Republik mengeluarkan video hasil kecerdasan buatan yang berisi sindiran kepada calon presiden dari Partai Demokrat sekaligus petahana Joe Biden. "What if the weakest president we've ever had were re-elected (Bagaimana jika, Presiden terlemah yang kita punya, terpilih kembali)" tulis salah satu narasinya. Darrel M. West, pengajar senior di Center for Technology Innovation, Brookings Institution, AS, mengungkapkan AI kini benar-benar siap dipakai dalam kampanye. "Tiga tahun lalu, AI benar-benar tidak digunakan dalam kampanye pemilihan. Tetapi teknologi telah berkembang sangat pesat. Sekarang, teknologinya sudah siap," kata dia. Menurutnya, para politisi dapat menggunakan AI generatif untuk merespons dengan cepat. Dalam kasus Komite Nasional Partai Republik itu, videonya dirilis tepat setelah pengumuman kembali pencalonan Biden. (can/dmi)"""

    from pysbd import Segmenter
    segmenter = Segmenter(language='en', clean=True)
    sents = segmenter.segment(rtext)
    sents[0] = utils.cleaner(sents[0].split('--')[1])
    data = " ".join(sents)
    return {
        'detail': data
    }


@router.get("/", response_model=simple_schema.Simple)
async def sentiment():
    return {"detail": "Welcome to Intelligence Socio Analysis (ISA)"}