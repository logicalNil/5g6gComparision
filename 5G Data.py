import simpy
import random
import pandas as pd

# Define simulation parameters
SIM_DURATION = 1000  # simulation duration in seconds
NUM_DEVICES = 1000  # number of end devices in the network
SERVICE_RATE = 1.0 / 10.0  # average service rate of network devices in seconds
INTER_ARRIVAL_TIME = 1.0 / 20.0  # average inter-arrival time of packets in seconds


# Define a function to simulate packet transmissions in a 5G network
def packet_transmission(env, source, destination):
    # Generate a random packet size
    packet_size = random.randint(100, 1000)

    # Send the packet to the destination
    yield env.timeout(packet_size * SERVICE_RATE)

    # Generate random priority and traffic class
    priority = random.randint(1, 5)
    traffic_class = random.choice(['VoIP', 'Video Streaming', 'Web Browsing'])

    # Record the end-to-end delay
    end_to_end_delay = env.now - source

    # Return the end-to-end delay, priority, and traffic class
    return end_to_end_delay, priority, traffic_class


# Define a function to simulate end devices in a 5G network
def end_device(env, device_id):
    while True:
        # Generate a new packet
        packet = (env.now, device_id, random.randint(1, NUM_DEVICES))

        # Send the packet to the destination
        end_to_end_delay, priority, traffic_class = yield env.process(packet_transmission(env, packet[0], packet[2]))

        # Record the end-to-end delay in a dataset
        data.append({
            "Packet ID": len(data) + 1,
            "Source": packet[1],
            "Destination": packet[2],
            "End-to-End Delay": end_to_end_delay,
            "Priority": priority,
            "Traffic Class": traffic_class
        })

        # Wait for the next packet arrival
        yield env.timeout(random.expovariate(INTER_ARRIVAL_TIME))


# Initialize the simulation environment
env = simpy.Environment()

# Initialize the dataset
data = []

# Create end devices
for i in range(NUM_DEVICES):
    env.process(end_device(env, i))

# Run the simulation
env.run(until=SIM_DURATION)

# Save the dataset to a CSV file
df = pd.DataFrame(data)
df.to_csv("end_to_end_delay_6g.csv", index=False)