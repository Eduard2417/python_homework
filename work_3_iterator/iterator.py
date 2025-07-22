from dataclasses import dataclass
import math


class Fibonacci:

    def __init__(self, length: int):
        self.per_value = 1
        self.value = 0
        self.length = length

    def __iter__(self):
        return self

    def __next__(self):
        result = self.per_value + self.value
        self.per_value = self.value
        self.value = result

        if self.length == 0:
            raise StopIteration

        self.length -= 1
        return result

    @staticmethod
    def generate_elements(length: int):
        fib = Fibonacci(length)
        elements = [element for element in fib]
        return elements


@dataclass
class Page:
    page: int
    next_page: int
    data: list


@dataclass
class Query:
    page: int
    page_elements: int


class ApiResponse:

    def __init__(self, query: Query, length: int):
        self.query = query
        self.max_generate = (math.ceil(length / query.page_elements) + 1
                             ) - self.query.page
        self.elements = Fibonacci.generate_elements(length)

    def response(self):
        start_index = (self.query.page - 1) * self.query.page_elements
        end_index = start_index + self.query.page_elements
        data = self.elements[start_index:end_index]
        page = Page(self.query.page, self.query.page + 1, data)
        self.query.page += 1
        return page


def request(api_obj: ApiResponse):
    for _ in range(api_obj.max_generate):
        yield api_obj.response()


api = ApiResponse(Query(3, 6), 14)
generator = request(api)
