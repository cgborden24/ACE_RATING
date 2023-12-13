import pandas as pd
import openpyxl
import time
import schedule
from datetime import datetime
import math
import statistics
import numpy as np
import threading
from sqlalchemy import create_engine
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
pd.set_option('mode.chained_assignment', None)

run_loop = True

def job():
    class NBAPlayerAnalyzer:
        def __init__(self, year, fg_weight=9.0, threept_weight=5.0, twopt_weight=0.00,
                    trb_weight=9.0, ast_weight=8.5, stl_weight=0.00, blk_weight=0.00,
                    pts_weight=10, ws_weight=41, usg_weight=0.00):
            self.year = year
            self.fg_weight = fg_weight
            self.threept_weight = threept_weight
            self.twopt_weight = twopt_weight
            self.trb_weight = trb_weight
            self.ast_weight = ast_weight
            self.stl_weight = stl_weight
            self.blk_weight = blk_weight
            self.pts_weight = pts_weight
            self.ws_weight = ws_weight
            self.usg_weight = usg_weight

            self.rbo_values = []

        def fetch_current(self):
            total_df = pd.read_html(f'https://www.basketball-reference.com/leagues/NBA_{self.year}_totals.html')[0]
            columns_to_convert_to_int = ['G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%',
                                            '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 
                                            'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
            total_df[columns_to_convert_to_int] = total_df[columns_to_convert_to_int].apply(pd.to_numeric, errors='coerce', axis=1)
            total_df = total_df.dropna()
            advanced_df = pd.read_html(f'https://www.basketball-reference.com/leagues/NBA_{self.year}_advanced.html')[0]
            columns_to_convert_to_int = ['Rk', 'Player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'PER', 'TS%', '3PAr',
                                        'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
                                        'Unnamed: 19', 'OWS', 'DWS', 'WS', 'WS/48', 'Unnamed: 24', 'OBPM',
                                        'DBPM', 'BPM', 'VORP']
            advanced_df[columns_to_convert_to_int] = advanced_df[columns_to_convert_to_int].apply(pd.to_numeric, errors='coerce', axis=1)
            total_df['WS'] = advanced_df[['WS']]
            total_df['WS/48'] = advanced_df[['WS/48']]
            total_df['USG%'] = advanced_df[['USG%']]
            formula_df = total_df.drop(['MP','Rk', 'Tm','Pos','Age','FG','FGA','ORB','DRB','TOV','PF','3PA','2PA','FT','FTA','FT%'], axis=1)
            formula_df['Player'] = formula_df['Player'].str.rstrip('*')

            max_fg_percentage = formula_df['FG%'].max()
            fg_percentage_ratio = formula_df['FG%']/max_fg_percentage

            max_threept = formula_df['3P'].max()
            threept_ratio = formula_df['3P']/max_threept

            max_twopt = formula_df['2P'].max()
            twopt_ratio = formula_df['2P']/max_twopt

            max_trb = formula_df['TRB'].max()
            trb_ratio = formula_df['TRB']/max_trb

            max_ast = formula_df['AST'].max()
            ast_ratio = formula_df['AST']/max_ast

            max_stl = formula_df['STL'].max()
            stl_ratio = formula_df['STL']/max_stl

            max_blk = formula_df['BLK'].max()
            blk_ratio = formula_df['BLK']/max_blk

            max_pts = formula_df['PTS'].max()
            pts_ratio = formula_df['PTS']/max_pts

            max_ws = formula_df['WS'].max()
            ws_ratio = formula_df['WS']/max_ws

            max_usg = formula_df['USG%'].max()
            usg_ratio = formula_df['USG%']/max_usg

            formula_df['ACE'] = (
                (self.fg_weight * (formula_df['FG%'] * fg_percentage_ratio)) +
                (self.threept_weight * (formula_df['3P'] * threept_ratio)) +
                (self.twopt_weight * (formula_df['2P'] * twopt_ratio)) +
                (self.trb_weight * (formula_df['TRB'] * trb_ratio)) +
                (self.ast_weight * (formula_df['AST'] * ast_ratio)) +
                (self.stl_weight * (formula_df['STL'] / max_stl)) +
                (self.blk_weight * (formula_df['BLK'] / max_blk)) +
                (self.pts_weight * (formula_df['PTS'] * pts_ratio)) +
                (self.ws_weight * (formula_df['WS'] * ws_ratio)) +
                (self.usg_weight * (formula_df['USG%'] * max_usg))
            )


            formula_df = formula_df.sort_values(by='ACE', ascending=False)

            formula_df['ratiogame'] = formula_df['G'] / formula_df['G'].max()

            #formula_df = formula_df[formula_df['ratiogame'] >= 0.7].dropna()

            return formula_df

        def fetch_data(self):

            file_name = f'SourceStats_{self.year}.xlsx'

            formula_df = pd.read_excel(file_name)

            formula_df['Player'] = formula_df['Player'].str.rstrip('*')

            max_fg_percentage = formula_df['FG%'].max()
            fg_percentage_ratio = formula_df['FG%']/max_fg_percentage

            max_threept = formula_df['3P'].max()
            threept_ratio = formula_df['3P']/max_threept

            max_twopt = formula_df['2P'].max()
            twopt_ratio = formula_df['2P']/max_twopt

            max_trb = formula_df['TRB'].max()
            trb_ratio = formula_df['TRB']/max_trb

            max_ast = formula_df['AST'].max()
            ast_ratio = formula_df['AST']/max_ast

            max_stl = formula_df['STL'].max()
            stl_ratio = formula_df['STL']/max_stl

            max_blk = formula_df['BLK'].max()
            blk_ratio = formula_df['BLK']/max_blk

            max_pts = formula_df['PTS'].max()
            pts_ratio = formula_df['PTS']/max_pts

            max_ws = formula_df['WS'].max()
            ws_ratio = formula_df['WS']/max_ws

            max_usg = formula_df['USG%'].max()
            usg_ratio = formula_df['USG%']/max_usg

            formula_df['ACE'] = (
                ((self.fg_weight) * (fg_percentage_ratio))  +
                ((self.threept_weight) * (threept_ratio)) +
                ((self.twopt_weight) * (twopt_ratio)) +
                ((self.trb_weight) * (trb_ratio)) +
                ((self.ast_weight) * (ast_ratio)) +
                ((self.stl_weight) * (max_stl)) +
                ((self.blk_weight) * (max_blk)) +
                ((self.pts_weight) * (pts_ratio)) +
                ((self.ws_weight) * (ws_ratio)) +
                ((self.usg_weight) * (max_usg)) 
            )
            
            formula_df = formula_df.sort_values(by='ACE', ascending=False)

            formula_df['ratiogame'] = formula_df['G'] / formula_df['G'].max()

            formula_df = formula_df[formula_df['ratiogame'] >= 0.7].dropna()

            formula_df = formula_df.head(8)

            return formula_df

        def save_to_excel(self, data):
            with pd.ExcelWriter(f'output_{self.year}.xlsx', engine = 'openpyxl') as writer:
                data.to_excel(writer, sheet_name=str(self.year), index=False)
                writer.book.active = 0

        def save_to_sql(self, data):
            db_connection_str = 'postgresql://postgres:password@localhost:5432/Capstone'
            engine = create_engine(db_connection_str)
            data.to_sql(f'nba_data_{self.year}', engine, if_exists='replace', index=False)

        def save_to_sql2(self,data):
            db_connection_str = 'postgresql://postgres:password@localhost:5432/Capstone'
            engine = create_engine(db_connection_str)
            data.to_sql('history_ACE', engine, if_exists='replace', index=False)

        def RBO(self, List1, List2, p):
            answer = 0
            for i in range(8):
                answer += math.pow(p,i+1)/(i+1) * len(set(List1[0:i+1]) & set(List2[0:i+1]))
            return answer*(1-p)

        def combine_results(self, start_year, end_year):
            result_dfs = []

            for year in range(start_year, end_year + 1):
                file_name = f'output_{year}.xlsx'

                try:
                    # Specify the engine parameter as 'openpyxl'
                    formula_df = pd.read_excel(file_name, engine='openpyxl')
                except Exception as e:
                    print(f"Error reading {file_name}: {e}")
                    continue  # Skip to the next iteration if an error occurs

                formula_df['ACEyear'] = str(year)

                result_dfs.append(formula_df)

            result_df = pd.concat(result_dfs, ignore_index=True)

            return result_df



        def analyze_current(self):
            total_data = self.fetch_current()
            top_players = total_data['Player'].tolist()

            self.save_to_sql(total_data)
            self.save_to_excel(total_data)

            return top_players

        def analyze(self):
            total_data = self.fetch_data()
            filtered_data = total_data[total_data['ACE'] >= 0.7]

            top_players = filtered_data['Player'].tolist()

            self.save_to_sql(filtered_data)
            self.save_to_excel(filtered_data)

            combined_results = self.combine_results(1991, 2023)

            self.save_to_sql2(combined_results)

            return top_players


    class MVPanalyzer:
        def __init__(self, year):
            self.year = year

        def fetch_data(self):
            file_name = f'mvp_{self.year}.xlsx'
            formula_df = pd.read_excel(file_name)
            ranking = formula_df.head(8)
            return ranking

        def save_to_excel(self, data):
            with pd.ExcelWriter(f'mvp_{self.year}.xlsx') as writer:
                data.to_excel(writer, sheet_name=str(self.year), index=False)

        def save_to_sql(self, data):
            db_connection_str = 'postgresql://postgres:password@localhost:5432/Capstone'
            engine = create_engine(db_connection_str)
            data.to_sql(f'mvp_{self.year}', engine, if_exists='replace', index=False)

        def save_to_sql2(self, data):
            db_connection_str = 'postgresql://postgres:password@localhost:5432/Capstone'
            engine = create_engine(db_connection_str)
            data.to_sql('history_MVP', engine, if_exists='replace', index=False)

        def combine_results(self, start_year, end_year):
            result_dfs = []

            for year in range(start_year, end_year + 1):
                file_name = f'mvp_{year}.xlsx'

                try:
                    # Specify the engine parameter as 'openpyxl'
                    formula_df = pd.read_excel(file_name, engine='openpyxl')
                except Exception as e:
                    print(f"Error reading {file_name}: {e}")
                    continue  # Skip to the next iteration if an error occurs

                formula_df['ACEyear'] = str(year)

                result_dfs.append(formula_df)

            result_df = pd.concat(result_dfs, ignore_index=True)

            return result_df

        def analyze(self):
            mvp_data = self.fetch_data()
            top_mvp_players = mvp_data['Player'].tolist()
            combined_results = self.combine_results(1991, 2023)
            self.save_to_sql2(combined_results)
            return top_mvp_players


    years = list(range(2023, 1990, -1))

    currentyear_analyzer = NBAPlayerAnalyzer(2024)
    current_result = currentyear_analyzer.analyze_current()

    for year in years:
        mvp_analyzer = MVPanalyzer(year)
        mvp_result = mvp_analyzer.analyze()
        player_analyzer = NBAPlayerAnalyzer(year)
        result = player_analyzer.analyze()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%m/%d/%Y")
    
    print("last executed:", current_day,"at", current_time)
    
#schedule.every(10).seconds.do(job)
schedule.every(1).days.at("06:00").do(job) 

def schedule_thread():
    while True:
        run_loop = True

        while run_loop:
            schedule.run_pending()
            time.sleep(1)

        print('Loop has been exited.')
        time.sleep(10)  # Adjust this sleep time as needed

# Start the scheduling thread
schedule_thread = threading.Thread(target=schedule_thread)
schedule_thread.start()

# Allow the job to run for a certain duration (e.g., 30 seconds)
time.sleep(10)

# Stop the scheduling thread
schedule_thread.join()