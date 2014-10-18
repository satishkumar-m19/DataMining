#!/usr/bin/python
import string
import sys

class DataCube:
    users_data ={}
    jobs_data ={}
    base_cuboid = []
    def __init__(self):
        self.users_data ={}
        self.jobs_data ={}
        self.base_cuboid = []
        
    def process_users_data(self,f_users):
        f_users.next()
        for line in f_users:
            data = line.strip().split('\t')
            dict_users = {data[0]:{'state':data[2],'country':data[3]}}
            self.users_data.update(dict_users)

    def process_jobs_data(self,f_jobs):   
        f_jobs.next()
        for line in f_jobs:
            data = line.strip().split('\t')
            dict_users = {data[0]:{'title':data[1]}}
            self.jobs_data.update(dict_users)

    def create_base_cuboid(self,f_apps):
        f_apps.next()
        for line in f_apps:
            data = line.strip().split('\t')
            dict_struct = {}
            dict_struct["userid"],dict_struct["jobid"] = data[0],data[2]
            dict_struct['state'],dict_struct["country"] = dict(self.users_data.get(data[0])).get('state'),dict(self.users_data.get(data[0])).get('country')
            try:
                dict_struct['title'] = dict(self.jobs_data.get(data[2],None)).get('title')
            except:
                dict_struct['title'] = ' '
            self.base_cuboid.append(dict_struct)
        
class DataCubeOperations(DataCube):
    def __init__(self):
        self.user_app_list = {}
        self.count_apptit_list = {}
        
    def higher_level_cuboid(self):
        for data in self.base_cuboid:
            self.user_app_list.setdefault((data.get('state'),data.get('country'),data.get('jobid')),[]).append(data.get('userid'))
            self.count_apptit_list.setdefault((data.get('country'),data.get('title')),[]).append(data.get('jobid'))
    
    def state_job_wise_cuboid(self):
        self.state_count = []
        for each_state in self.user_app_list:
            self.state_count.append([len(self.user_app_list.get(each_state)),each_state])
        self.state_count.sort(reverse=True)
        print "Problem 1 : "
        print ('stateId\tJobId\tnumOfApps').expandtabs(15)
        for each in self.state_count[:5]:
            print (`each[1][0]` +'\t'+ `each[1][2]` +'\t'+ `each[0]`).expandtabs(15)
    
    def country_title_wise_cuboid(self,country = 'US'): 
        self.country_app_count = []
        for each_country in self.count_apptit_list:
            if each_country[0]==country:
                self.country_app_count.append([len(self.count_apptit_list.get(each_country)),each_country])
        self.country_app_count.sort(reverse=True)
        print '\nProblem 2 : ' 
        print ('TitleId\tnumOfApps').expandtabs(50)
        for each in self.country_app_count[:5]:
            print (`each[1][1]` + '\t' + `each[0]`).expandtabs(50)

def main():
#     f_users = open("/home/sati/CSE-5334/programming-assignment/users.tsv")
#     f_apps = open("/home/sati/CSE-5334/programming-assignment/apps.tsv")
#     f_jobs = open("/home/sati/CSE-5334/programming-assignment/jobs.tsv")
  
    f_apps = open(sys.argv[2])
    f_users = open(sys.argv[3])
    f_jobs = open(sys.argv[4])    
    country = sys.argv[1]
     
    data_cube = DataCubeOperations()
    data_cube.process_users_data(f_users)
    data_cube.process_jobs_data(f_jobs)
    data_cube.create_base_cuboid(f_apps)
      
    data_cube.higher_level_cuboid()
    '''  Call to the methods for the 1st problem  '''
    data_cube.state_job_wise_cuboid()
    '''  Call to the methods for the 2nd problem  '''
    data_cube.country_title_wise_cuboid(country)

if __name__ == '__main__':
    main()
