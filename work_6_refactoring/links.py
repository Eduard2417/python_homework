from datetime import datetime, date

from bs4 import BeautifulSoup


def is_valid_href(href: str) -> bool:
    """Проверяет корректность ссылки"""
    return "/upload/reports/oil_xls/oil_xls_" in href and href.endswith(".xls")


def extract_date_from_href(href: str) -> date:
    """Извлекает дату из ссылки и возвращает в виде объекта date"""
    date_str = href.split("oil_xls_")[1][:8]
    return datetime.strptime(date_str, "%Y%m%d").date()


def build_full_url(href: str) -> str:
    """Проверяет ссылку 'href' и возвращает полный URL,
    добавляя префикс "https://spimex.com", если он отсутствует.
    """
    return href if href.startswith("http") else f"https://spimex.com{href}"


def parse_page_links(html: str, start_date: date,
                     end_date: date, url: str) -> list:
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls"
    href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:

        if not hasattr(link, 'get'):
            continue

        href = link.get("href", "")
        href = href.split("?")[0]

        if not is_valid_href(href):
            continue

        try:
            file_date = extract_date_from_href(href)
            if start_date <= file_date <= end_date:
                full_url = build_full_url(href)
                results.append((full_url, file_date))
            else:
                print(f"Ссылка {href} вне диапазона дат")
        except ValueError as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results
