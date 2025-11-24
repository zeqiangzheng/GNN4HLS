#!/usr/bin/python
import xmltodict

def extract_rtl_timing(xml_file):
    with open(xml_file) as fd:
        # read the report in xml format
        doc = xmltodict.parse(fd.read())

        # old implementation, using number of cycles only
        #avg_latency = int(doc['profile']['PerformanceEstimates']['SummaryOfOverallLatency']['Average-caseLatency'])

        # parse the result to find the percentage usage of the resources
        dsp = int(doc['profile']['AreaReport']['Resources']['DSP'])
        ff = int(doc['profile']['AreaReport']['Resources']['FF'])
        lut = int(doc['profile']['AreaReport']['Resources']['LUT'])
        bram = int(doc['profile']['AreaReport']['Resources']['BRAM'])

        dsp_avail = int(doc['profile']['AreaReport']['AvailableResources']['DSP'])
        ff_avail = int(doc['profile']['AreaReport']['AvailableResources']['FF'])
        lut_avail = int(doc['profile']['AreaReport']['AvailableResources']['LUT'])
        bram_avail = int(doc['profile']['AreaReport']['AvailableResources']['BRAM'])

        dsp_perc = dsp / dsp_avail
        ff_perc = ff / ff_avail
        lut_perc = lut / lut_avail
        bram_perc = bram / bram_avail

        # extract the period/frequency, for now, we assume the unit is always ns

        try:
          period = float(doc['profile']['TimingReport']['AchievedClockPeriod'])  # can be NA
        except:
          period = ""
        
        # parse the report to find the latency
        # new implementation, using the real-time latency
        # result = doc['profile']['PerformanceEstimates']['SummaryOfOverallLatency']['Average-caseRealTimeLatency'].split()
        # avg_latency = float(result[0])

        report = (dsp, ff, lut, bram, \
                  dsp_avail, ff_avail, lut_avail, bram_avail, \
                  dsp_perc, ff_perc, lut_perc, bram_perc, \
                  period)

        return report