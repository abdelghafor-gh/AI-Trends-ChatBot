from mit_news.scraper import MITNewsScraper
from ieee_spectrum.scraper import IEEESpectrumScraper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def inspect_mit_news():
    print("\n=== Inspecting MIT News AI Feed ===")
    scraper = MITNewsScraper()
    scraper.inspect_feed_structure(sample_size=2)

def inspect_ieee_spectrum():
    print("\n=== Inspecting IEEE Spectrum AI Feed ===")
    scraper = IEEESpectrumScraper()
    scraper.inspect_feed_structure(sample_size=2)

if __name__ == "__main__":
    inspect_mit_news()
    print("\n" + "="*50 + "\n")
    inspect_ieee_spectrum()
