import datetime, math

def find_components(components, project_id):
    lst = []
    for comp in components:
        if comp['project'] == project_id:
            lst.append(comp)

    return lst


def get_remaining_fund(cost, actual_cost, budget_ratio, completion):
    if actual_cost == 0:
        return cost * budget_ratio
    
    completion /= 100.0
    completion_rem = 1 - completion


def load_agency_fund_constraints(agencies, constraints):
    agency_fund = {}
    
    for constraint in constraints:
        if constraint['constraint_type'] == 'yearly_funding':
            agency_fund[constraint['code']] = float(constraint['max_limit'])
    
    for agency in agencies:
        if agency['code'] not in agency_fund.keys():
            agency_fund[agency['code']] = None

    return agency_fund


def load_location_constraints(constraints):
    location_limit = {}
    for constraint in constraints:
        if constraint['constraint_type'] == 'location_limit':
            location_limit[constraint['code']] = int(constraint['max_limit'])

    return location_limit


def load_agency_limit_constraints(constraints):
    agency_limit = {}
    for constraint in constraints:
        if constraint['constraint_type'] == 'executing_agency_limit':
            agency_limit[constraint['code']] = int(constraint['max_limit'])

    return agency_limit


def get_span(timespan, completion):
    return math.ceil((100 - completion) * timespan * 365.0 / 100.0)

def calculate_end_time(projects, constraints, components, agencies):

    pcomps = []

    agency_limit = load_agency_limit_constraints(constraints)

    agency_fund = load_agency_fund_constraints(agencies, constraints)
    
    location_limit = load_location_constraints(constraints)

    # print(agency_fund)

    at = 0
    for project in projects:
        comp_list = find_components(components, project['id'])
        for comp in comp_list:
            pcomps.append((comp, at, project['completion']))
            if not agency_fund[project['exec']] == None:
                agency_fund[project['exec']] -= float(project['actual_cost']) * float(comp['budget_ratio'])
        
        at += 1

    
    # print(agency_fund)

    today = datetime.date.today()

    # print(today)

    end_date = {}

    running_projects = []
    comp_state = {}
    cnt = {}

    for comp in pcomps:
        comp_state[comp[0]['id']] = 'PAUSED'

    days_passed = -1

    while days_passed <= 700:
        days_passed += 1

        # print(days_passed, len(running_projects))

        flag = True
        count = 0
        for key in comp_state.keys():
            if comp_state[key] == 'PAUSED' or comp_state[key] == 'RUNNING':
                flag = False
                count += 1

        if flag == True:
            break
        
        # print(count)
        # if count <= 67:
        #     print(comp_state)
        #     break

        cur_date = today + datetime.timedelta(days = days_passed)
        if cur_date.month == 1 and cur_date.day == 1:
            agency_fund = load_agency_fund_constraints(agencies, constraints)

        while True:
            sel_comp, sel_span = None, None

            for comp in pcomps:
                start_date = datetime.datetime.strptime(projects[comp[1]]['start_date'], '%Y-%m-%d').date()
                if(cur_date < start_date):
                    continue
                if comp_state[comp[0]['id']] == 'PAUSED':
                    agency_id = projects[comp[1]]['exec']
                    if agency_id not in agency_limit.keys() or agency_limit[agency_id] > 0:
                        location = projects[comp[1]]['location']
                        if location not in location_limit.keys() or location_limit[location] > 0:
                            if comp[0]['depends_on'] == None or comp_state[comp[0]['depends_on']] == 'DONE':
                                cur_span = get_span(projects[comp[1]]['timespan'], comp[2])
                                if sel_comp == None or cur_span < sel_span:
                                    sel_comp = comp
                                    sel_span = cur_span

            if sel_comp == None:
                break
            else :
                running_projects.append((sel_comp, sel_span))
                comp_state[sel_comp[0]['id']] = 'RUNNING'
                
                if projects[sel_comp[1]]['exec'] in agency_limit.keys():
                    agency_limit[projects[sel_comp[1]]['exec']] -= 1
                
                if projects[sel_comp[1]]['location'] in location_limit.keys():
                    location_limit[projects[sel_comp[1]]['location']] -= 1

        to_del = []

        for i in range(0, len(running_projects)):
            comp = running_projects[i][0]
            days_rem = running_projects[i][1]

            # if projects[comp[1]]['project_id'] == 'proj1644':
            #     print(comp[0]['id'], days_rem, cur_date)
            
            project_cost = projects[comp[1]]['cost']
            
            if projects[comp[1]]['completion'] != 0:
                project_cost = max(project_cost, projects[comp[1]]['actual_cost'] * 100.0 / projects[comp[1]]['completion'] )
            daily_cost = project_cost / (365 * projects[comp[1]]['timespan'])

            daily_cost =  float(daily_cost) * float(comp[0]['budget_ratio'])

            agency_id = projects[comp[1]]['exec']
            location = projects[comp[1]]['location']

            if agency_fund[agency_id] == None or daily_cost < agency_fund[agency_id]:
                days_rem -= 1
                running_projects[i] = (comp, days_rem)
                if not agency_fund[agency_id] == None:
                    agency_fund[agency_id] -= daily_cost

                if days_rem  == 0:
                    to_del.append(running_projects[i])
                    comp_state[comp[0]['id']] = 'DONE'
                    if agency_id in agency_limit.keys():
                        agency_limit[agency_id] += 1
                    
                    if location in location_limit.keys():
                        location_limit[location] += 1
                    
                    # print(cur_date)
                    end_date[projects[comp[1]]['id']] = cur_date
                    
                    if projects[comp[1]]['id'] not in cnt.keys():
                        cnt[projects[comp[1]]['id']] = 1
                    else :
                        cnt[projects[comp[1]]['id']] += 1
            else :
                to_del.append(running_projects[i])
                comp_state[comp[0]['id']] = 'PAUSED'
                if agency_id in agency_limit.keys():
                    agency_limit[agency_id] += 1
                    
                if location in location_limit.keys():
                    location_limit[location] += 1
                for i in range (0, len(pcomps)):
                    if pcomps[i][0] == comp[0]:
                        pcomps[i] = (pcomps[i][0], pcomps[i][1], 100 - (100 * days_rem / (365 * projects[comp[1]]['timespan'])))
                        break

        
        for item in to_del:
            running_projects.remove(item)
                                
        # print(cur_date)
        # days_passed += 1

    # print(len(end_date))
    for key in end_date.keys():
        if cnt[key] < 2 :
            continue
        for project in projects:
            if project['id'] == key:
                start_date = datetime.datetime.strptime(project['start_date'], '%Y-%m-%d').date()
                # print(end_date, today)
                print(project['project_id'], end_date[key] - today, 365.0 * project['timespan'] * (100 - project['completion']) / 100.0)
                break



    # return {project_id, end_time}

    # print(projects, constraints, components)