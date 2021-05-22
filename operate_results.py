#operate_results.py
import numpy as np
import pandas as pd

#we check it every second
#takes to do 0.01 sec
def clear_stream(data_source='/Users/argosaakan/Data/proryv/wifi_data_move.csv', aim_mac='34:da:b7:f5:7d:02'):
    #time_mark = time.time()
    df = pd.read_csv(data_source, sep=', ', header=None, engine='python')
    rssis = df[3].str.split('-', expand=True)
    rssis.rename(columns={1: 'rssi'}, inplace=True)

    subtypes = df[1].str.split('=', expand=True)
    subtypes.rename(columns={1: 'subtype'}, inplace=True)

    macs1 = df[4].str.split('=', expand=True)
    macs1.rename(columns={1: 'mac1'}, inplace=True)

    macs2 = df[5].str.split('=', expand=True)
    macs2.rename(columns={1: 'mac2'}, inplace=True)

    macs3 = df[6].str.split('=', expand=True)
    macs3.rename(columns={1: 'mac3'}, inplace=True)


    final = pd.DataFrame(rssis['rssi']).join(pd.DataFrame(subtypes['subtype'])).join(pd.DataFrame(macs1['mac1'])).join(pd.DataFrame(macs2['mac2'])).join(pd.DataFrame(macs3['mac3']))
    final['rssi'] = final['rssi'].astype(int)
    probes = final.loc[final['subtype'] == '40']['rssi'].tolist()

    final = final.loc[final['mac2'] == aim_mac]
    final = final.loc[final['mac1'] == 'ff:ff:ff:ff:ff:ff']

    data = final['rssi'].tolist()

    if len(probes) == 0:
        return {'Beacon_RSSI': data, 'Beacon_av_RSSI': np.average(data), 'Beacon_disp_RSSI': np.disp(data),
            'Probe_RSSI': probes, 'Probe_av_RSSI': None, 'Beacon_disp_RSSI': None}
    #print(time.time() - time_mark)
    return {'Beacon_RSSI': data, 'Beacon_av_RSSI': np.average(data), 'Beacon_disp_RSSI': np.var(data),
            'Probe_RSSI': probes, 'Probe_av_RSSI': np.average(probes), 'Probe_disp_RSSI': np.var(probes)}

def analize_data(data_dict):
    norm_RSSI_t = 50
    norm_RSSI_p = 50
    norm_disp_t = 10
    norm_disp_p = 50
    if data_dict['Beacon_av_RSSI'] > norm_RSSI_t:
        if data_dict['Beacon_disp_RSSI'] > norm_disp_t:
            t_status = 'active'
        else:
            t_status = 'empty road'
    else:
        if data_dict['Beacon_disp_RSSI'] > norm_disp_t:
            t_status = 'heavy'
        else:
            t_status = 'traffic jam'

    if data_dict['Probe_av_RSSI'] < norm_RSSI_p:
        if data_dict['Probe_disp_RSSI'] > norm_disp_p:
            p_status = 'heavy'
        else:
            p_status = 'citizen jam)'
    else:
        if data_dict['Probe_disp_RSSI'] > norm_disp_p:
            p_status = 'active'
        else:
            p_status = 'no people'
    return {'traffic':t_status, 'people':p_status}

def define_transport_types(data_dict):
    #NN or statisctics to define number
    #NN to define types
    #NN should be traines - we will use BiLSTM+CNN neural networks
    pass

if __name__=='__main__':
    print(analize_data(clear_stream()))
