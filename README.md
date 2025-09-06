# Pusula_Liva_Nur_Karanfil

**Ad Soyad:** Liva Nur Karanfil  
**E-posta:** <karanfillivanur@gmail.com>

## Proje Özeti
Bu depo, Fizik Tedavi ve Rehabilitasyon (PM&R) alanındaki **2235 gözlem** ve **13 özellikten** oluşan veri kümesi için Keşifsel Veri Analizi (EDA) ve **model öncesi veri hazırlama** (temizleme, standardizasyon, özellik mühendisliği) adımlarını içerir. Bu çalışma **model kurmayı zorunlu kılmaz**; odak, hedef değişken **`TedaviSuresi`** etrafında veriyi **temiz, tutarlı ve analiz edilebilir** hâle getirmektir.

## Veri Kümesi Sütunları
- `HastaNo`: Anonim hasta ID’si  
- `Yas`: Yaş  
- `Cinsiyet`: Cinsiyet  
- `KanGrubu`: Kan grubu  
- `Uyruk`: Uyruk  
- `KronikHastalik`: Kronik hastalıklar (virgülle ayrılmış liste)  
- `Bolum`: Bölüm/Klinik  
- `Alerji`: Alerjiler (tekli veya virgüllü liste)  
- `Tanilar`: Tanılar  
- `TedaviAdi`: Tedavi adı  
- `TedaviSuresi`: Tedavi süresi (seans) **[Hedef]**  
- `UygulamaYerleri`: Uygulama bölgeleri  
- `UygulamaSuresi`: Uygulama süresi

> Not: Veri örnek adları ve içerik yapısı kurum politikalarına göre maskelenmiş/anonimleştirilmiş olabilir.

## Dizin Yapısı
```
Pusula_Liva_Nur_Karanfil/
├─ data/
│  ├─ raw/                # ham veri (ör. dataset.csv)
│  └─ processed/          # temizlenmiş/özelliklendirilmiş veri çıktıları
├─ notebooks/
│  ├─ 01_eda.ipynb        # EDA
│  └─ 02_preprocessing.ipynb
├─ src/
│  ├─ preprocessing.py     # temizleme & özellik mühendisliği
│  └─ utils.py             # yardımcı fonksiyonlar
├─ reports/
│  ├─ figures/             # grafik ve görseller
│  └─ Bulgular_Ozeti.md    # (opsiyonel) bulgular dokümanı
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## Kurulum
### 1) Ortam
- Python 3.10+ (öneri: 3.11)
- Sanal ortam (venv) önerilir

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` tipik olarak şunları içerir:
```
pandas
numpy
matplotlib
seaborn
scikit-learn
pyyaml
jupyter
```

### 2) Veriyi Yerleştirme
Ham veri dosyanızı `data/raw/` içine koyun (örn. `dataset.csv`).

## Çalıştırma
### Seçenek A — Jupyter Notebook
```bash
jupyter notebook
```
- `notebooks/01_eda.ipynb` dosyasını açın ve hücreleri sırayla çalıştırın.
- Ardından `notebooks/02_preprocessing.ipynb` içinde temizleme ve özellik mühendisliği adımlarını yürütün.

### Seçenek B — Komut Satırı (opsiyonel)
```bash
python src/preprocessing.py   --input data/raw/dataset.csv   --output data/processed/dataset_clean.csv   --config configs/preprocess.yaml
```
> `configs/preprocess.yaml` içinde kategori kodlamaları, eksik değer stratejileri, eşik değerleri vb. tanımlanabilir.

## Uygulanan Başlıca Adımlar
- **İsimlendirme standardizasyonu**: sütun adlarının sadeleştirilmesi (küçük harf, Türkçe karakterler vb.).
- **Eksik değer işlemleri**: numerik (örn. medyan) ve kategorik (örn. “Bilinmiyor”) doldurma.
- **Çoklu-değerli alanların ayrıştırılması**: `KronikHastalik`, `Alerji`, `UygulamaYerleri` gibi virgüllü listelerin bölünmesi, sayısallaştırılması (örn. sayım özellikleri).
- **Kategori kodlama**: `Cinsiyet`, `KanGrubu`, `Uyruk`, `Bolum`, `TedaviAdi` gibi sütunlar için One-Hot/Target/Ordinal kodlama (bağlama göre).
- **Özellik mühendisliği**: yaş grupları, kronik/alerji sayıları, uygulama süresi/yer sayısı, tanı sayısı vb.
- **Hedef odaklı EDA**: `TedaviSuresi` dağılımı, uç değer analizi, önemli ilişkiler (örn. `Yas`, `KronikHastalik` sayısı, `UygulamaSuresi` ile korelasyon).
- **Çıktılar**: `data/processed/dataset_clean.csv` ve `reports/figures/` altında grafikler.

## GitHub’a Yükleme
Depo adınızın **tam olarak** şu desende olması gerekir: **`Pusula_Name_Surname`**  
Bu proje için: **`Pusula_Liva_Nur_Karanfil`**

Yeni depo oluşturma ve ilk gönderim:
```bash
git init
git add .
git commit -m "Initial commit: EDA + preprocessing + reports"
git branch -M main
git remote add origin https://github.com/<kullanici_adiniz>/Pusula_Liva_Nur_Karanfil.git
git push -u origin main
```

> Eğer yanlış bir uzak depo eklediyseniz veya “remote origin already exists” hatası alıyorsanız:
```bash
git remote set-url origin https://github.com/<kullanici_adiniz>/Pusula_Liva_Nur_Karanfil.git
git push -u origin main
```

## İletişim
Herhangi bir sorunuz için lütfen README başındaki e-posta adresinden iletişime geçin.

## Notlar
- Kişisel bilgileri, kurum politikaları gereği **anonim** tutun.
- Bulgularınızı ayrı bir dokümana işlediyseniz, `reports/Bulgular_Ozeti.md` olarak ekleyin ve **belgenin en üstüne ad-soyad ve e-postanızı** yazmayı unutmayın.
- Proje tamamlandığında **GitHub proje bağlantınızı aldığınız e-posta adresine** göndermeyi unutmayın.
