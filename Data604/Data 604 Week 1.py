''' 
Description:
All base measurements of time are in minutes

'''
# Packages that are needed
import simpy
import random
import statistics

# Contains the total amount of time each moviegoer spends
wait_times = []
print(wait_times)

class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

# It takes 1-3 mins in order to purchase a ticket
    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1,3))

# It takes 3 seconds for ushers to check a ticket
    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

# It takes 1-5 mins for server to complete an order of food
    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1,5))

def go_to_movies(env, moviegoer, theater):
    # Moviegoer arrives at the theater
    arrival_time = env.now
    
    # Checking if there is a cashier available
    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))
    

    # Going through the Usher to get tickets check
    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    # Deciding if the moviegoer wants food/drinks
    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))
    
    # Moviegoer heads into the theater
    wait_times.append(env.now - arrival_time)

def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater1 = Theater(env, num_cashiers, num_servers, num_ushers)

    # Expecting 3 moviegoer in line ready at start
    for moviegoer in range(3):
        env.process(go_to_movies(env, moviegoer, theater1))

    # Moviegoers arrive at theater every 12 seconds
    while True:
        yield env.timeout(0.20)

        moviegoer += 1 
        env.process(go_to_movies(env,moviegoer, theater1))

def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def calculate_wait_time(arrival_times, departure_times):
    average_wait = statistics.mean(wait_times)
    
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def get_user_input():
    num_cashiers = input("Input # of cashiers working:")
    num_servers = input("Input # of servers working:")
    num_ushers = input("Input # of ushers working:")
    params = [num_cashiers, num_servers, num_ushers]
    
    #####
    if all(str(i).isdigit() for i in params): # Checking input is valid
        params = [int(x) for x in params]
    else: 
        print(
            "Could not parse input. The simulation will use default values:",
            "\n1 cashier, 1 server, 1 usher."  
        )
        params = [1,1,1]
    return params

def main():
    # Setup
    random.seed(334)
    num_cashiers, num_servers, num_ushers = get_user_input()

    # Running Simulation
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers,num_ushers))
    env.run(until = 90)

    # View the results
    mins, secs = get_average_wait_time(wait_times)
    print(
        "Running simulation..."
        f"\nThe average wait time is {mins} minutes and {secs} seconds."
    )

if __name__ == '__main__':
    main()