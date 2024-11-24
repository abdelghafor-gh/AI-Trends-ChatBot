# AI Trends ChatBot

A modern AI-powered chatbot that provides insights about the latest AI trends and news. The application consists of three main components:

1. Next.js Frontend - A modern, responsive chat interface
2. n8n Backend - Workflow automation for processing and managing chat interactions
3. Azure Functions - Data scraping scripts for collecting AI news from various RSS feeds

## Project Structure

```
AI-Trends-ChatBot/
├── frontend/               # Next.js frontend application
├── n8n-workflows/         # n8n workflow configurations
└── azure-functions/       # Azure Functions for RSS scraping
    └── rss-scraper/      # RSS feed scraping function
```

## Setup Instructions

### Frontend Setup (Next.js)
1. Navigate to the frontend directory
```bash
cd frontend
npm install
npm run dev
```

### n8n Setup
1. Install n8n globally
```bash
npm install n8n -g
```
2. Start n8n
```bash
n8n start
```
3. Import the workflow configurations from the n8n-workflows directory

### Azure Functions Setup
1. Install Azure Functions Core Tools
2. Navigate to azure-functions directory
3. Deploy the functions using Azure CLI
```bash
az login
az functionapp deploy
```

## RSS Feed Sources

#### [SiliconANGLE - AI](https://siliconangle.com/category/ai/)

- RSS Feed: [siliconangle.com/category/ai/feed/](https://siliconangle.com/category/ai/feed/)

#### [Amazon Science](https://www.amazon.science/)

- RSS Feed: [amazon.science/index.rss](https://www.amazon.science/index.rss)

#### [Analytics India Magazine (AIM) | Artificial Intelligence, And Its Commercial, Social And Political Impact](https://analyticsindiamag.com/)

- Rss feed: [analyticsindiamag.com/feed/](https://analyticsindiamag.com/feed/)

#### [AI News - Artificial Intelligence News](https://www.artificialintelligence-news.com/)

- RSS Feed: [artificialintelligence-news.com/feed/](https://www.artificialintelligence-news.com/feed/)

#### [Google DeepMind](https://deepmind.google/discover/blog/)

- RSS Feed: [deepmind.google/blog/rss.xml](https://deepmind.google/blog/rss.xml)

#### [Microsoft Research – Emerging Technology, Computer, and Software Research](https://www.microsoft.com/en-us/research/)

- RSS Feed: [microsoft.com/en-us/research/feed/](https://www.microsoft.com/en-us/research/feed/)

#### [Artificial intelligence | MIT News | Massachusetts Institute of Technology](https://news.mit.edu/topic/artificial-intelligence2)

- RSS Feed: [news.mit.edu/topic/mitartificial-intelligence2-rss.xml](https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml)

#### [AI News &amp; Artificial Intelligence | TechCrunch](https://techcrunch.com/category/artificial-intelligence/)

- RSS Feed: [techcrunch.com/category/artificial-intelligence/feed/](https://techcrunch.com/category/artificial-intelligence/feed/)

#### [Artificial Intelligence - Dataconomy](https://dataconomy.com/category/topics/data-science/artificial-intelligence/)

- RSS Feed: [dataconomy.com/category/topics/data-science/artificial-intelligence/feed/](https://dataconomy.com/category/topics/data-science/artificial-intelligence/feed/)

#### [Blog – Google Research](https://research.google/blog/)

#### [AI Business Informs, educates and connects the global AI community](https://aibusiness.com/)

- RSS Feed: [aibusiness.com/rss.xml](https://aibusiness.com/rss.xml)

#### [Last Week in AI | Substack](https://lastweekin.ai/)

- RSS Feed: [lastweekin.ai/feed](https://lastweekin.ai/feed)

#### [HackerNoon - read, write and learn about any technology](https://hackernoon.com/)

- RSS Feed: [hackernoon.com/tagged/ai/feed](https://hackernoon.com/tagged/ai/feed)

#### [News on Artificial Intelligence and Machine Learning](https://techxplore.com/machine-learning-ai-news/)

- RSS Feed: [techxplore.com/rss-feed/machine-learning-ai-news/](https://techxplore.com/rss-feed/machine-learning-ai-news/)

#### [Artificial Intelligence: News, Business, Science | THE DECODER](https://the-decoder.com/)

- RSS Fedd: [the-decoder.com/feed/](https://the-decoder.com/feed/)

#### [Artificial intelligence (AI) | The Guardian](https://www.theguardian.com/technology/artificialintelligenceai)

- RSS Feed: [theguardian.com/technology/artificialintelligenceai/rss](https://www.theguardian.com/technology/artificialintelligenceai/rss)

#### [Artificial Intelligence - The Verge](https://www.theverge.com/ai-artificial-intelligence)

- RSS Feed: [theverge.com/ai-artificial-intelligence/rss/index.xml](https://www.theverge.com/ai-artificial-intelligence/rss/index.xml)

#### [AI News &amp; Robotics News - Unite.AI](https://www.unite.ai/)

- RSS Feed: [unite.ai/feed/](https://www.unite.ai/feed/)

#### [AI News | VentureBeat](https://venturebeat.com/category/ai/)

- RSS Feed: [venturebeat.com/category/ai/feed/](https://venturebeat.com/category/ai/feed/)

#### [AI + ML News • The Register](https://www.theregister.com/software/ai_ml/)

- RSS Feed: [theregister.com/software/ai_ml/headlines.atom](https://www.theregister.com/software/ai_ml/headlines.atom)

#### [AI, ML &amp; Data Engineering for Software Developers - InfoQ](https://www.infoq.com/ai-ml-data-eng/)

- RSS Feed: [feed.infoq.com/ai-ml-data-eng/](https://feed.infoq.com/ai-ml-data-eng/)

#### [Import AI](https://jack-clark.net/)

- RSS Feed: [jack-clark.net/feed/](https://jack-clark.net/feed/)

#### [News | Last Week in AI | Substack](https://lastweekin.ai/s/news)

- RSS Feed:

#### [IEEE Spectrum](https://spectrum.ieee.org/)

- RSS Feed: [spectrum.ieee.org/feeds/topic/artificial-intelligence.rss](https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss)

#### [Home - MarkTechPost](https://www.marktechpost.com/)

- RSS Feed: [marktechpost.com/feed/](https://www.marktechpost.com/feed/)

#### [AI Accelerator Institute | Future of artificial intelligence](https://www.aiacceleratorinstitute.com/)

- RSS Feed: [aiacceleratorinstitute.com/rss/](https://www.aiacceleratorinstitute.com/rss/)

#### [Ars Technica - Category: AI](https://arstechnica.com/ai/)

- RSS Feeds: [RSS Feeds - Ars Technica](https://arstechnica.com/rss-feeds/)
- Tech Rss Feed: [feeds.arstechnica.com/arstechnica/technology-lab](https://feeds.arstechnica.com/arstechnica/technology-lab)

#### [Synced](https://syncedreview.com/)

- RSS Feed: [syncedreview.com/feed/](https://syncedreview.com/feed/)

#### [Artificial Intelligence | Extremetech](https://www.extremetech.com/tag/artificial-intelligence)

#### [Machine Learning ML &amp; Generative AI News](https://www.reddit.com/r/machinelearningnews/)

- API json: [reddit.com/r/machinelearningnews.json?limit=50](https://www.reddit.com/r/machinelearningnews.json?limit=50)

#### [ΑΙhub | Connecting the AI community and the world](https://aihub.org/category/news/)

- RSS Feed: [aihub.org/category/news/feed/](https://aihub.org/category/news/feed/)

#### [AI - AI-Tech Park](https://ai-techpark.com/ai/)

- RSS Feed: [ai-techpark.com/feed/](https://ai-techpark.com/feed/)

## Features
- Real-time chat interface
- AI trend analysis and insights
- Automated news collection and processing
- Natural language processing for better user interactions

## Tech Stack
- Frontend: Next.js 13, React, TailwindCSS
- Backend: n8n for workflow automation
- Data Collection: Azure Functions, Node.js
- Database: MongoDB (for storing processed news and chat history)

## Contributing
Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License
MIT License
