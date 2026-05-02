# Linux File Permissions Explained
## Permission Basics
Örnek: -rw-r--r-- 1 user group 1024 Apr 27 10:00 file.txt

- Birinci karakter: - (dosya), d (klasör)
- Sonraki 3: Owner (sahip) izinleri
- Sonraki 3: Group (grup) izinleri  
- Sonraki 3: Other (diğerleri) izinleri

## Permission Values
- r (read) = 4
- w (write) = 2
- x (execute) = 1

## Örnekler
- 755 = rwxr-xr-x (owner: tüm, others: okuma+çalıştırma)
- 644 = rw-r--r-- (owner: okuma+yazma, others: okuma)
- 700 = rwx------ (sadece owner)

## Komutlar
chmod 755 dosya.sh     # Çalıştırılabilir yap
chmod 644 dosya.txt    # Normal dosya
chmod +x script.sh     # Execute ekle
chown user dosya.txt   # Sahibi değiştir
