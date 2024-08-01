import gymnasium as gym
from gymnasium import spaces
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import carla
import numpy as np
import random
import itertools
import math
import time as tm

# Define the discrete values for speed and direction
speed_values = np.linspace(1.0, 1.5, num=10)  # 10 speeds between 1.0 and 1.5 m/s
direction_values = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]  # Directions in radians

# Create all possible combinations of the discrete action values
discrete_actions = list(itertools.product(speed_values, direction_values))

class CarlaPedestrianEnv(gym.Env):
    def __init__(self, spawn_point_idx=0):
        super(CarlaPedestrianEnv, self).__init__()
        self.client = carla.Client('127.0.0.1', 2000)
        self.client.set_timeout(2.0)
        self.world = self.client.get_world()
        self.blueprint_library = self.world.get_blueprint_library()
        self.pedestrian = None
        self.av = None
        self.spent_time = 0
        self.spawn_point_idx = spawn_point_idx+4
        self.setup_environment()

        # Use the number of discrete actions
        self.action_space = spaces.Discrete(len(discrete_actions))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)

    def setup_environment(self):
        pedestrian_bp = random.choice(self.blueprint_library.filter('walker.pedestrian.*'))
        # spawn_points = self.world.get_map().get_spawn_points()
        # spawn_point = spawn_points[self.spawn_point_idx % len(spawn_points)]
        spawn_point = random.choice(self.world.get_map().get_spawn_points())
        self.pedestrian = self.world.spawn_actor(pedestrian_bp, spawn_point)

        for actor in self.world.get_actors().filter('vehicle.*'):
            if actor.attributes.get('role_name') == "host_vehicle":
                self.av = actor

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if self.pedestrian:
            self.pedestrian.destroy()
        self.setup_environment()

        pedestrian_transform = self.pedestrian.get_transform()
        av_transform = self.av.get_transform()

        state = self.get_state(pedestrian_transform, av_transform)
        return np.array(state, dtype=np.float32), {}

    def step(self, action):
        # Map the discrete action to the continuous action
        self.spent_time += 1
        continuous_action = discrete_actions[action]
        
        speed = continuous_action[0]*5*4
        direction_angle = continuous_action[1]

        control = carla.WalkerControl()
        control.speed = speed

        # Compute direction vector from angle
        direction_x = math.cos(direction_angle)
        direction_y = math.sin(direction_angle)

        control.direction = carla.Vector3D(x=direction_x, y=direction_y, z=0.0)
        self.pedestrian.apply_control(control)
        
        initial_position = self.pedestrian.get_transform().location
        for _ in range(5):  # Adjust the range for the required time delay
            self.world.tick()
        new_position = self.pedestrian.get_transform().location

        moved_distance = initial_position.distance(new_position)
        if moved_distance < 0.1:
            for _ in range(5):  # Adjust the range for the required time delay
                self.world.tick()

        pedestrian_transform = self.pedestrian.get_transform()
        av_transform = self.av.get_transform()

        state = self.get_state(pedestrian_transform, av_transform)
        reward = self.calculate_reward(pedestrian_transform, av_transform, initial_position, new_position)
        done = self.check_done(pedestrian_transform, av_transform)

        return np.array(state, dtype=np.float32), reward, done, False, {}

    def get_state(self, pedestrian_transform, av_transform):
        pedestrian_location = pedestrian_transform.location
        av_location = av_transform.location
        max_distance = 50.0
        distance = pedestrian_location.distance(av_location) / max_distance
        
        direction_to_av = np.arctan2(av_location.y - pedestrian_location.y, av_location.x - pedestrian_location.x)
        pedestrian_orientation = pedestrian_transform.rotation.yaw
        return [pedestrian_location.x, pedestrian_location.y, av_location.x, av_location.y, distance, direction_to_av, pedestrian_orientation]

    def calculate_reward(self, pedestrian_transform, av_transform, initial_position, new_position):
        pedestrian_location = pedestrian_transform.location
        av_location = av_transform.location
        distance = math.fabs(pedestrian_location.distance(av_location))

        previous_distance = math.fabs(initial_position.distance(av_location))
        new_distance = math.fabs(new_position.distance(av_location))
        reduction = previous_distance - new_distance
        reward = 0
        if reduction > 0:
            reward += reduction*10
        else:
            reward += reduction
        
        reward -= 0.01 
        # print(reward, self.spent_time)

        # Reward for getting closer to the vehicle
        if distance < 4.0:
            reward += 1000

        return reward

    def check_done(self, pedestrian_transform, av_transform):
        pedestrian_location = pedestrian_transform.location
        av_location = av_transform.location
        distance = pedestrian_location.distance(av_location)

        if self.spent_time > 1000:
            self.spent_time = 0
            return True            

        if distance < 4.0:
            self.spent_time = 0
            return True
        else:
            return False

    def render(self, mode='human'):
        pass

    def close(self):
        if self.pedestrian:
            self.pedestrian.destroy()

# Factory function to create environments
def make_env(rank):
    def _init():
        env = CarlaPedestrianEnv(spawn_point_idx=rank)
        env = Monitor(env)  # Wrap with Monitor to log rewards
        # env.seed(seed)
        return env
    return _init

if __name__ == "__main__":
    
    try:
        # Number of parallel environments
        num_envs = 1

        # Create the vectorized environment
        env = SubprocVecEnv([make_env(i) for i in range(num_envs)])

        model = PPO('MlpPolicy', env, verbose=2)

        model = PPO.load(f"/media/william/mist2/william/UDrive/Part2/stablebaselines3/savedModels/PPO/ppo_pedestrian_checkpoint2", env=env)
        # model.learn(total_timesteps=50000)

        # # Save the model
        # model.save("/media/william/mist2/william/UDrive/Part2/stablebaselines3/savedModels/PPO/ppo_pedestrian_checkpoint2.zip")

        

        # Use the model for inference
        obs = env.reset()
        for i in range(1000):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, _ = env.step(action) # return np.array(state, dtype=np.float32), reward, done, False, {}
            # print(reward)
            if done:
                obs = env.reset()
    finally:
        # Ensure proper cleanup
        if 'env' in locals():
            try:
                env.close()
            finally:
                print("completed")

    
