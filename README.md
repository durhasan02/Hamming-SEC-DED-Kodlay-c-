# Hamming SEC-DED Kod Simülatörü

Bu proje, 8, 16 ve 32 bitlik veriler üzerinde Hamming SEC-DED (Single Error Correcting, Double Error Detecting) kodunu simüle eden, kullanıcı dostu bir Python/Tkinter uygulamasıdır.

## Özellikler
- 8, 16, 32 bitlik veri girişi
- Hamming kodu oluşturma (SEC-DED)
- Belleğe yazma ve okuma
- İstenilen bit üzerinde yapay hata oluşturma
- Hatalı biti sendrom ile tespit etme ve düzeltme
- Bitleri kutucuklar içinde görsel olarak gösterme

## Ekran Görüntüsü

Ana ekran örneği:

![Ana Ekran](�PNG

)

## Kurulum

1. Python 3 yüklü olmalı.
2. Gerekli kütüphaneler (sadece Tkinter, Python ile birlikte gelir):

```bash
python main.py
```

## Kullanım

1. Bit uzunluğunu seçin (8, 16, 32).
2. Binary veri girin (ör: `10110011`).
3. "Kodla" butonuna basarak Hamming kodunu oluşturun.
4. "Belleğe Yaz" ile kodu belleğe kaydedin.
5. "Bellekten Oku" ile kodu tekrar görüntüleyin.
6. "Hata Ekle" ile istediğiniz bit pozisyonunda yapay hata oluşturun.
7. "Düzelt" ile hatalı biti tespit edip düzeltin.

## Koddan Örnekler

```python
# Hamming kodu oluşturma
hamming_code = self.hamming_encode(data)
self.show_result(f"Girdi: {data}\nHamming Kodu: {hamming_code}", bits=hamming_code)

# Hata ekleme
code[pos] = '1' if code[pos] == '0' else '0'
self.memory = ''.join(code)
self.show_result(f"{pos}. bit terslendi!\nYeni veri: {self.memory}", bits=self.memory, error_index=pos)

# Hata düzeltme
if syndrome != 0:
    code[syndrome] = '1' if code[syndrome] == '0' else '0'
    self.memory = ''.join(code)
    self.show_result(result, bits=code, error_index=syndrome)
```

 
