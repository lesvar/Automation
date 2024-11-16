from credentials import *
import pandas as pd


def get_traffic_bytes(ASK, start_date, end_date, name='bytes-by-time', version=1):
    # Set up request headers and parameters
    headers = {
         "Accept": "application/json",
         "PAPI-Use-Prefixes": "true"
    }
    qs = {
        'accountSwitchKey': ASK,
        "start": start_date + 'T00:00:00.000Z', 
        "end":  end_date + 'T00:00:00.000Z',
        'interval': 'DAY',
        'allObjectIds': 'true',
        'metrics': 'bytesOffloadAvg,bytesOffloadMax,bytesOffloadMin,bytesOffloadSlope, edgeBitsPerSecondMax, edgeBitsPerSecondMin,edgeBytesSlope,edgeBytesTotal, midgressBitsPerSecondMax, midgressBitsPerSecondMin, midgressBytesSlope, midgressBytesTotal,originBitsPerSecondMax, originBitsPerSecondMin, originBytesSlope, originBytesTotal, bytesOffloadTotal  '        
    }
    path = '/reporting-api/v1/reports/{}/versions/{}/report-data'.format(name, version)
    # Make the API request
    response = session.get(urljoin(baseurl, path), headers = headers, params=qs)
    if response.status_code == 200 :
        return response.json()
    else:
        return f"Failed to retrieve json data error: {response.status_code}"


def get_traffic_hits(ASK, start_date, end_date, name='hits-by-time', version=1):
    # Set up request headers and parameters
    headers = {
         "Accept": "application/json",
         "PAPI-Use-Prefixes": "true"
    }
    qs = {
        'accountSwitchKey': ASK,
        "start": start_date + 'T00:00:00.000Z', 
        "end":  end_date + 'T00:00:00.000Z', 
        'interval': 'DAY',
        'allObjectIds': 'true', 
        'metrics': 'edgeHitsPerSecondMax,edgeHitsPerSecondMin,edgeHitsSlope,edgeHitsTotal,hitsOffloadAvg,hitsOffloadMax,hitsOffloadMin,hitsOffloadSlope,originHitsPerSecondMax,originHitsPerSecondMin,originHitsSlope,originHitsTotal,hitsOffloadTotal'        
    }
    path = '/reporting-api/v1/reports/{}/versions/{}/report-data'.format(name, version)
    # Make the API request
    response = session.get(urljoin(baseurl, path), headers = headers, params=qs)
    if response.status_code == 200 :
        return response.json()
    else:
        return f"Failed to retrieve json data error: {response.status_code}"

def extract_data_metrics(results):
    metrics = []
    data_list= []
    
    # retrieve string vals in summary stat
    for item in results:
        metrics.append(item)
        for val in results[item].items():
            if isinstance(val,str):
                data_list.append(val)
    
    # combining data and metrics in a specifc format for pandas
    combined_list = list(zip(metrics,data_list))
    return combined_list

def export_data_excel(ASK, end_date, result_hbt, result_bbt):
    result_stat1 = result_hbt["summaryStatistics"]
    result_stat2 = result_bbt["summaryStatistics"]
    hits_results = extract_data_metrics(result_stat1)
    bytes_results = extract_data_metrics(result_stat2)

    
    print("--------------------------------------")
    #data to be exported in 3 separate sheets
    hits_file_name= f"{ASK}.{end_date}.hits-by-time.xlsx"
    df =pd.DataFrame(hits_results)
    df.to_excel(hits_file_name,index=False, header=False)
    print("Excel fie created with CP codes that have data for hits by time!")
    
    bytes_file_name= f"{ASK}.{end_date}.bytes-by-time.xlsx"
    df2 =pd.DataFrame(bytes_results)
    df2.to_excel(bytes_file_name,index=False, header=False)
    print("Excel fie created with CP codes that have data for bytes by time!")
    
    file_name= f"{ASK}.latest.by-time.xlsx"
    df3 = pd.concat([df, df2], axis=0, ignore_index=True)
    df3.to_excel(file_name,index=False, header=False)
    print("Excel fie created with CP codes that have data for latest by time!")



if __name__ == '__main__':
    print(generate_switch_key())
    # requesting user input
    ASK = input('Enter the account switch key:\n')
    start_date = input('Enter the start date in format YYYY-MM-FD:\n') 
    end_date = input('Enter the end date in format YYYY-MM-LD:\n')
    # data pulled
    result_hbt = get_traffic_hits(ASK, start_date, end_date)
    result_bbt = get_traffic_bytes(ASK, start_date, end_date)
    export_data_excel(ASK, end_date, result_hbt, result_bbt)
    
        