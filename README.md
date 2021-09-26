# nss - Nessus Scanner Scanner

A python based nessus scanner scanner and bruteforcer for discovering open nessus scanners 

Has Censys API support to allow for speedy host discovery 

USAGE: ./nss.py -i input_hostsfile -o output_file -d dictionary_file -use_censys
        -d -- Dictonary file, supply list of passwords in text file format
        -i -- Input file, list of hosts supplied in either masscan -oG format OR list of IPs 
        -o -- output file, in text format
        -use_censys -- flag to use censys for host discovery (if used, API key and Secret required to be added)
        

