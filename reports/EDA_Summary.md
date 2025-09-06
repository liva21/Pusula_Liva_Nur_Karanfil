# EDA Summary
- Dataset: `data/Talent_Academy_Case_DT_2025.xlsx`
- Shape: 2235 x 20
- Numeric columns (excl. id/target): ['Yas', 'UygulamaSuresi_min']
- Figures: `outputs/figures/`, `outputs/figures_target/`

## Target Summary — TedaviSuresi
**Raw target (sessions):**
```
count    2235.000000
mean       14.570917
std         3.725322
min         1.000000
25%        15.000000
50%        15.000000
75%        15.000000
max        37.000000
```
**Winsorized target (sessions):**
```
count    2235.000000
mean       14.509620
std         3.469818
min         2.000000
25%        15.000000
50%        15.000000
75%        15.000000
max        25.000000
```

## Robust Aggregations (min count ≥ 30) — 2025-09-06 19:32
### Bolum
```
                                                count       mean  median
Bolum                                                                   
Fiziksel Tıp Ve Rehabilitasyon,Solunum Merkezi   2045  15.136430    15.0
İç Hastalıkları                                    32   9.437500    10.0
Ortopedi Ve Travmatoloji                           88   4.818182     4.0
```

### Cinsiyet
```
          count       mean  median
Cinsiyet                          
Kadin      1274  14.771586    15.0
Erkek       792  14.406566    15.0
```

### KanGrubu
```
          count       mean  median
KanGrubu                          
B+          206  14.771845    15.0
0+          579  14.411054    15.0
AB+          80  14.350000    15.0
B-           68  14.176471    15.0
A-           53  14.018868    15.0
A+          540  14.003704    15.0
```

### Uyruk
```
         count       mean  median
Uyruk                            
Türkiye   2173  14.509434    15.0
```

### TedaviAdi
```
                        count       mean  median
TedaviAdi                                       
Dorsalji 1                140  15.857143    15.0
Dorsalji-Dorsal            56  15.535714    15.0
Gonartroz-Meniskopati      95  15.473684    15.0
Dorsalji -Boyun+trapez    231  15.454545    15.0
İV DİSK BOZUKLUĞU-BEL     200  15.025000    15.0
SAĞ OMUZ İMPİNGEMENT       70  15.000000    15.0
Sol Omuz İmpingement       30  15.000000    15.0
Dorsalji-Bel              120  14.666667    15.0
Sol omuz İmpingement       50  14.500000    15.0
Boyun-Trapezz              60  14.166667    15.0
```

## Robust Aggregations with Winsorized Target (min count ≥ 30) — 2025-09-06 19:32
### Bolum
```
                                                count       mean  median
Bolum                                                                   
Fiziksel Tıp Ve Rehabilitasyon,Solunum Merkezi   2045  15.078240    15.0
İç Hastalıkları                                    32   9.437500    10.0
Ortopedi Ve Travmatoloji                           88   4.840909     4.0
```

### Cinsiyet
```
          count       mean  median
Cinsiyet                          
Kadin      1274  14.678179    15.0
Erkek       792  14.383838    15.0
```

### KanGrubu
```
          count       mean  median
KanGrubu                          
B+          206  14.679612    15.0
AB+          80  14.350000    15.0
0+          579  14.343696    15.0
B-           68  14.176471    15.0
A-           53  14.018868    15.0
A+          540  13.966667    15.0
```

### Uyruk
```
         count       mean  median
Uyruk                            
Türkiye   2173  14.464795    15.0
```

### TedaviAdi
```
                        count       mean  median
TedaviAdi                                       
Dorsalji-Dorsal            56  15.535714    15.0
Gonartroz-Meniskopati      95  15.473684    15.0
Dorsalji 1                140  15.428571    15.0
Dorsalji -Boyun+trapez    231  15.367965    15.0
İV DİSK BOZUKLUĞU-BEL     200  15.025000    15.0
SAĞ OMUZ İMPİNGEMENT       70  15.000000    15.0
Sol Omuz İmpingement       30  15.000000    15.0
Dorsalji-Bel              120  14.666667    15.0
Sol omuz İmpingement       50  14.500000    15.0
Boyun-Trapezz              60  14.166667    15.0
```
