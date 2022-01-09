import httplib2
import apiclient.discovery
import settings

from oauth2client.service_account import ServiceAccountCredentials
from movie_service import MovieService


class GoogleSheetsService:
    def __init__(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            settings.CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)

    def start(self):
        data = self._get_movie_names()
        for i, movie in enumerate(data):
            movie_service = MovieService(movie)
            if i != 0:
                movie_data = movie_service.get_full_movie_info()
                try:
                    movie_info = [
                        [
                            movie_data['rating'],
                            movie_data['duration'],
                            movie_data['year'],
                            movie_data['director']
                        ]
                    ]
                    self._insert_movie_info(i, movie_info)
                    print(movie_info)
                except TypeError:
                    print('type error')

    def _get_movie_names(self):
        data = self.service.spreadsheets().values().get(
            spreadsheetId=settings.spreadsheet_id,
            range='A1:A1000',  # movie names cells
            majorDimension='ROWS'
        ).execute()['values']
        return data

    def _insert_movie_info(self, movie_index, movie_info):
        self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=settings.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        'range': f'G{movie_index + 1}:J{movie_index + 1}',
                        'majorDimension': "ROWS",
                        'values': movie_info
                    }
                ]
            }
        ).execute()
