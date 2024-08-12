from pprint import pprint

from src.fakedata.fake_genre import FakeGenreData


bulk_query = FakeGenreData().generate_genres(3)
pprint(bulk_query)
pprint([{'_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
  '_index': 'genres',
  '_source': {'description': '',
              'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
              'name': 'Action'}},
 {'_id': '120a21cf-9097-479e-904a-13dd7198c1dd',
  '_index': 'genres',
  '_source': {'description': '',
              'id': '120a21cf-9097-479e-904a-13dd7198c1dd',
              'name': 'Adventure'}}])