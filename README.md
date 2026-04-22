# Open WebUI 👋

[![GitHub Stars](https://img.shields.io/github/stars/open-webui/open-webui?style=social)](https://github.com/open-webui/open-webui&stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/open-webui/open-webui?style=social)](https://github.com/open-webui/open-webui/network/members)
[![GitHub Watchers](https://img.shields.io/github/watchers/open-webui/open-webui?style=social)](https://github.com/open-webui/open-webui/watchers)
[![Discord](https://img.shields.io/badge/Discord-Open%20WebUI-blue?logo=discord)](https://discord.gg/5rJgQTnV4s)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Pulls](https://img.shields.io/docker/pulls/ghcr.io/open-webui/open-webui)](https://github.com/open-webui/open-webui/pkgs/container/open-webui)

**Open WebUI**, tamamen çevrimdışı çalışabilen, kendi sunucunuza kurulabilen, genişletilebilir ve kullanımı kolay bir yapay zeka arayüz platformudur. [Ollama](https://ollama.com) ve **OpenAI uyumlu API**'leri tam olarak destekler.

📚 **Dokümantasyon:** [docs.openwebui.com](https://docs.openwebui.com)
💬 **Discord:** [discord.gg/5rJgQTnV4s](https://discord.gg/5rJgQTnV4s)

---

## ✨ Ana Özellikler

- 🖥️ **Sezgisel Arayüz** — ChatGPT'ye benzer, kullanımı kolay sohbet arayüzü; duyarlı tasarım ve tam mobil uyumluluk
- 📱 **Progressive Web App (PWA)** — Mobil cihazlarda yerel uygulama deneyimi; çevrimdışı erişim desteği
- ✍️ **Tam Markdown & LaTeX Desteği** — Zengin metin biçimlendirme ve matematiksel ifadeler için kapsamlı destek
- 🎤 **Sesli / Görüntülü Konuşma** — Dahili konuşma tanıma ve sentezi; görüntülü iletişim desteği
- 🔍 **Web Arama** — Çeşitli sağlayıcılar aracılığıyla web araması yapma ve sonuçları sohbete entegre etme
- 🤖 **Çoklu Model Desteği** — Birden fazla yapay zeka modeli arasında sorunsuz geçiş ve karşılaştırma
- 📂 **RAG (Retrieval-Augmented Generation)** — Belge ve dosyalarınızı yapay zekaya bağlayın; doküman tabanlı zeka
- 🛠️ **Araç & Fonksiyon Desteği** — Özel araçlar ve fonksiyonlarla yapay zekanın yeteneklerini genişletin
- 👥 **Çok Kullanıcılı Yönetim** — Kullanıcı hesapları, roller ve erişim denetimiyle güvenli çok kullanıcılı ortam
- 🔒 **Güvenli İzin Sistemi** — Ayrıntılı rol tabanlı izin kontrolü ve yönetici paneli
- 🎨 **Özelleştirilebilir Tema** — Açık/koyu mod ve kişiselleştirilebilir arayüz seçenekleri
- 💾 **Konuşma Geçmişi** — Tüm sohbetler yerel olarak saklanır; arama, dışa aktarma ve içe aktarma desteği
- 🌐 **Ollama & OpenAI Uyumlu** — Ollama modelleri ve OpenAI API'siyle tam entegrasyon
- 🐳 **Docker & Kubernetes Desteği** — Kolay kurulum ve ölçeklendirme için konteyner desteği

---

## 🚀 Hızlı Başlangıç

### Docker ile Kurulum (Önerilen)

**Ollama ile birlikte (aynı sunucuda):**

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

**Yalnızca OpenAI API ile:**

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_KEY=your_api_key \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

**CUDA (GPU) desteğiyle:**

```bash
docker run -d -p 3000:8080 --gpus all \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:cuda
```

Kurulum tamamlandıktan sonra tarayıcınızda [http://localhost:3000](http://localhost:3000) adresine gidin.

---

## 📦 Kurulum Yöntemleri

### 1. pip ile Kurulum

```bash
pip install open-webui
open-webui serve
```

### 2. Docker Compose ile Kurulum

```yaml
# docker-compose.yml
version: '3'
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    restart: always
    extra_hosts:
      - "host.docker.internal:host-gateway"

volumes:
  open-webui:
```

```bash
docker compose up -d
```

### 3. Manuel Kurulum (Geliştirici)

**Gereksinimler:** Python 3.11+, Node.js 20+

```bash
# Repoyu klonla
git clone https://github.com/open-webui/open-webui.git
cd open-webui

# Ön yüz bağımlılıkları
cp -RPp .env.example .env
npm install
npm run build

# Arka uç bağımlılıkları
cd backend
pip install -r requirements.txt -U

# Başlat
bash start.sh
```

---

## 🔧 Yapılandırma

Kurulum sonrası ilk çalıştırmada yönetici hesabı oluşturmanız istenecektir. Yönetici panelinden:

- Kullanıcı hesapları ve roller yönetilebilir
- Ollama / OpenAI API bağlantıları yapılandırılabilir
- Model ayarları ve varsayılan parametreler düzenlenebilir
- Araçlar, fonksiyonlar ve eklentiler yönetilebilir

Ayrıntılı yapılandırma için: [docs.openwebui.com](https://docs.openwebui.com)

---

## 🤝 Destek & İletişim

| Platform | Bağlantı |
|----------|----------|
| 📚 Dokümantasyon | [docs.openwebui.com](https://docs.openwebui.com) |
| 💬 Discord Topluluğu | [discord.gg/5rJgQTnV4s](https://discord.gg/5rJgQTnV4s) |
| 🐛 Hata Bildirimi | [GitHub Issues](https://github.com/open-webui/open-webui/issues) |
| 💡 Özellik İsteği | [GitHub Discussions](https://github.com/open-webui/open-webui/discussions) |
| ⭐ GitHub | [open-webui/open-webui](https://github.com/open-webui/open-webui) |

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakın.

---

<p align="center">
  Open WebUI ile yapay zekayı özgürce kullanın 🚀
</p>
