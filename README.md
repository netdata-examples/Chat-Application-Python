# Chat-Application-Python
#Netdata Sohbet Uygulaması
Sohbete bağlanan tüm kullanıcılarla anlık olarak sohbet edebileceğiniz bir chat uygulaması. Uygulama Netdata'nın sunduğu AccPo servis hizmetini kullanarak uygulama yenilemeden ve sürekli istek göndermeden anlık olarak mesajları kullanıcılara iletir. Ayrıca iletilen tüm veriler Netdata üzerinde oluşturulan projeye kaydedilir ve kullanıcı istediği zaman ulaşabilir.
Bu çalışmanın amacı Netdata üzerinden yapabileceklerinizin bir sınırının olmadığını göstermektir. Eğer netdata üzerinde bir projeniz varsa dışardan bu projenize erişip ekleme/silme/güncelleme gibi işlemleri Netdata'ya bağlı kalmaksızın yazdığınız uygulama içerisinde gerçekleştirebilirsiniz.
#Netdata üzerinden veri çekme
Netdata size birden fazla veri çekme yöntemi sunmaktadır. XML,JSON,SOAP Webservice ve IFRAME size sunduğumuz veri çekme yöntemleridir. Biz SOAP Webservice ile bağlantı kuracağız ve bunu için gerekli tanımlamaları static olarak programımıza yazacağız.
#Bağlantının Kurulması
Bağlantının kurulması için öncelikle global olarak xml isminde (veya istenilen bir isimde ) bir değişken oluşturulmalıdır. değişkenin global olarak oluşturulmasının sebebi bu değişkenle ile hem veri alacağız hem de veri göndereceğiz ve veri gönderme işlemi farklı fonksiyonlar tarafından da yapılabileceği için xml değişkeni global tanımlanmalıdır. Daha sonra request fonksiyonuna benzer bir fonksiyon hazırlanmalıdır. Bu fonksiyonda req = XML.replace('#kullaniciAdi#', Ui_MainWindow.kullaniciAdi).replace('#mesaj#', mesaj).replace('#AccPoApikodu#',                                                                                                             Ui_MainWindow.AccPoApikodu) burada oluşturduğumuz projenin AccPo Api kodunu ve xml verilerine ulaşmak için xml Api kodunu elle girememiz gerekmektedir.
Daha sonra request ile başlayan tüm fonsiyonlar GUI classımızın içinde oluşturulan def baglantıKur() fonksiyonu içerisinde yazılmalıdır.
```
def baglantıKur():
  req = XML.replace('#kullaniciAdi#',kullaniciAdi).replace('#mesaj#',mesaj).replace('#AccPoApikodu#',AccPoApikodu)
  cnn = httplib.HTTPConnection(HOST)
  cnn.request('POST', PAGE, req, HEADERS)
  res = cnn.getresponse().read()
```
