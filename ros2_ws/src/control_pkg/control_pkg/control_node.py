import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Int32, Float64MultiArray
import time

class Control(Node):
    def __init__(self):
        super().__init__("control_node")
        
        # ------------- CONSTANTS (sort of)

        self.MOTOR_FORWARD = 0
        self.MOTOR_RAMP = 1
        self.MOTOR_STAIR = 2
        self.MOTOR_LEFT_TURN = 3
        self.MOTOR_RIGHT_TURN = 4
        self.MOTOR_BIG_TURN = 5
        self.MOTOR_IDLE = 6
        self.MOTOR_KIT = 7
        self.MOTOR_FORCE_STOP = 8
        # little debugging things
        self.MOTOR_STATES = [self.MOTOR_IDLE, self.MOTOR_KIT]
        self.motor_test = 0

        self.HARMED = 2
        self.STABLE = 1
        self.UNHARMED = 0
        self.BACKGROUND = -1
        
        self.TILE_N = 2
        self.TILE_U = 1
        self.TILE_W = 0 

        # ------------ CONTROL NODE VARIABLES

        self.motor_ready = True
        self.camera_sees = "background"
        self.victim_status = self.BACKGROUND        

        self.STANDBY = 0
        self.MAPPING = 1
        self.TURNING = 2
        self.DRIVING = 3
        self.SCANNING = 4
        self.TURN_TO_SCAN = 5

        self.state = 0
        self.led_state = Bool()
        self.led_state.data = True

        self.hdg = 0
        self.pos = [0,0]
        self.tiles = {}
        self.target_hdg

        self.button_subscription = self.create_subscription(Bool, "button_topic", self.button_callback, 10)
        self.openmv_subscription = self.create_subscription(String, "openmv_data", self.camera_callback, 10)
        self.motor_status_sub = self.create_subscription(Bool, "motor_ready", self.status_callback, 10)

        self.led_publisher_ = self.create_publisher(Bool, "led_topic", 10)
        self.motor_publisher_ = self.create_publisher(Int32, "motor_topic",10)
        
        self.timer = self.create_timer(0.05, self.master_loop)

    # ------------ INPUT HANDLERS

    def button_callback(self, msg):
        if not msg.data: # IT'S WEIRD I THINK IT'S BACKWARDS... REMOVE THE not IF OTHERWISE
            # Button is pressed -> Cycle forwards one state
            self.state = (self.state + 1) % 3
            self.get_logger().info(f"Button pressed, changing state to {self.state}")

    def status_callback(self,msg):
        self.motor_ready = msg.data
    
    def camera_callback(self,msg):
        result = msg.data
        self.get_logger().info(f"Received: {result} from openmv_node")
        result = line.split(":")
        if result[0]=="Target":
            self.victim_status = int(result[1])
        else: # It's a letter
            match result[0]:
                case "phi":
                    self.victim_status = self.HARMED
                case "omega":
                    self.victim_status = self.UNHARMED
                case "psi":
                    self.victim_status = self.STABLE
                case _:
                    self.victim_status = self.BACKGROUND



    # ------------ CHECKING EVERY TICK FOR ACTIVE STATE (FSM CONTROL)... UM WHO KNOWS WHATS GOING IN HERE WE'LL FIND OUT...

    def master_loop(self):
        if self.state == self.STANDBY:
            return
        if not self.motor_ready:
            return
        match self.state:
            case self.MAPPING:
                self.execute_mapping()
            case self.TURNING:
                self.execute_turning()
            case self.DRIVING:
                self.execute_driving()
            case self.SCANNING:
                self.execute_scanning()
                # If theres more walls to scan I need to go to self.state = self.TURNTO SCAN
                # But if theres no more than I can go to self.TURNING (to leave) 
            case self.TURN_TO_SCAN:
                self.execute_turn_to_scan()

        # case self.ALGO:
        #     self.move()
        #     # Begin algorithm...?

        #     self.led_state.data = not self.led_state.data
            
        #     '''
        #     This kinda doesn't make sense here this little test CUZ its chewcking every .05 instead of every 5 now...
        #     '''
        #     # ------- Here's the logic to 


        #     self.motor_test = (self.motor_test + 1) % (len(self.MOTOR_STATES))
        #     self.msg = Int32()
        #     self.msg.data = self.MOTOR_STATES[self.motor_test]
        #     self.motor_publisher_.publish(self.msg)
        #     self.get_logger().info(f"Publishing: {self.msg.data} to motor_topic")

        #     case self.STOP:
        #         # Stop everything
        #         self.get_logger().info("STOP EVERYTHING RAHHHHHHHHHH!!!!!!")
        #         raise SystemExit



    # ---------- THINGS TO DO... idk if we need anything in here but making the section just in case its helpful

    def execute_mapping(self):
        self.get_logger().info(f"mapping tile at {self.pos}")

        self.update_map(self.pos[0], self.pos[1])

        max_score = self.score(self.pos[0] + 1, self.pos[1])
        
        self.target_hdg = 0

        if self.score(self.pos[0],self.pos[1] + 1) > max_score: # Check 90
            max_score = self.score(self.pos[0], self.pos[1] + 1)
            self.target_hdg = 180
        
        if self.score(self.pos[0] - 1, self.pos[1]) > max_score: # Check 180
            max_score = self.score(self.pos[0] - 1, self.pos[1])
            self.target_hdg = 180

        if self.score(self.pos[0], self.pos[1] - 1) > max_score: # Check 270
            self.target_hdg = 270

        self.state = self.TURN_TO_SCAN

    def execute_turn_to_scan(self):
        self.get_logger().info(f"turning to scan at tile at {self.pos}")

        for side in self.tiles[(self.pos[0],self.pos[1])]["sides"]:
            if side == self.TILE_W:
                ''' 
                # To turn to a certain heading basically you need to figure out 
                # whether you wanna turn RIGHT (4), LEFT (3), OR BIG (5)

                # depending on where you wanna turn , push
                cmd = Int32()
                cmd.data = # PUSH IT HERE THIS IS WHERE IT SHOULD GO
                self.motor_publisher_(cmd)
                time.sleep(3)
                '''
        
        self.state = self.SCANNING

    def execute_scanning(self):
        self.get_logger().info(f"scanning + dropping at tile at {self.pos}")
        # ALready be faced towards the direction I need to be just need to grab the victim variable
        match self.victim_status:
            case self.HARMED:
                # Drop two kits
                cmd = Int32()
                cmd.data = 9
                self.motor_publisher_.publish(cmd)
                self.led_publisher_.publish(self.led_state)
                self.get_logger().info(f"Publishing: {self.led_state} to led_topic")
            case self.STABLE:
                # Drop one kit
                cmd = Int32()
                cmd.data = 7
                self.motor_publisher_.publish(cmd)
                self.led_publisher_.publish(self.led_state)
                self.get_logger().info(f"Publishing: {self.led_state} to led_topic")
            case self.UNHARMED:
                self.led_publisher_.publish(self.led_state)
                self.get_logger().info(f"Publishing: {self.led_state} to led_topic")

        self.state = self.TURNING

    def execute_turning(self):
        turn_amount = (self.target_hdg - self.hdg) % 360

        if turn_amount == 0:
            self.state = self.DRIVING
            return

        self.get_logger().info(f"Turning {turn_amount}")
        cmd = Int32()
        match turn_amount:
            case 90:
                cmd.data = 4
            case 180:
                cmd.data = 5
            case 270:
                cmd.data = 3
        self.motor_publisher_.publish(cmd)

        self.hdg = self.target_hdg

        self.state = self.DRIVING
    
    def execute_driving(self):
        self.get_logger().info("Driving forward 1 tile")

        cmd = Int32()
        cmd.data = 0
        self.motor_publisher_.publish(cmd)

        match self.hdg: 
            case 0:
                self.pos[0] += 1
            case 90:
                self.pos[1] += 1
            case 180:
                self.pos[0] -=1
            case 270:
                self.pos[1] -= 1
        
        self.state = self.MAPPING
        
    # ----------- HELPER FUNCTIONS

    def new_tile(self, posx: int, posy: int, visited: bool, sides=None):
            if sides is None:
                sides = [self.U, self.U, self.U, self.U]
                
            if (posx, posy) not in self.tiles:
                self.tiles[(posx, posy)] = {"visited": visited, "sides": sides, "extra": ""}

    def update_map(self, posx, posy):
        self.tiles[(posx, posy)]["visited"] = True

        # Distance sensor...
        '''
        ADD....... THE............. DISTANCE SENSOR..... CALLBACKS....
        '''
        new_tiles_in_dirs = {
            (0 + self.hdg) % 360: self.tiles_front,
            (90 + self.hdg) % 360: self.tiles_left,
            (270 + self.hdg) % 360: self.tiles_right
        }
        if not 0 == (180+hdg)%360:    
            for new in range(new_tiles_in_dirs[0]):
                xc = self.pos[0]+new
                yc = self.pos[1]
                new_tile(xc,yc,False)
                tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_N
            xc = self.pos[0]+new_tiles_in_dirs[0]
            yc = self.pos[1]
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_W,self.TILE_N
                    
        if not 90 == (180+hdg)%360:    
            for new in range(new_tiles_in_dirs[90]):
                xc = self.pos[0]
                yc = self.pos[1]+new
                new_tile(xc,yc,False)
                tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3] = self.TILE_N,self.TILE_N
            xc = self.pos[0]
            yc = self.pos[1]+new_tiles_in_dirs[90]
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2] = self.TILE_W,self.TILE_N
            
        if not 180 == (180+hdg)%360:    
            for new in range(new_tiles_in_dirs[180]):
                xc = self.pos[0]-new
                yc = self.pos[1]
                new_tile(xc,yc,False)
                tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_N
            xc = self.pos[0]+new_tiles_in_dirs[180]
            yc = self.pos[1]
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][0],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_W
            
        if not 90 == (180+hdg)%360:    
            for new in range(new_tiles_in_dirs[90]):
                xc = self.pos[0]
                yc = self.pos[1]-new
                new_tile(xc,yc,False)
                tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][3] = self.TILE_N,self.TILE_N
            xc = self.pos[0]
            yc = self.pos[1]-new_tiles_in_dirs[270]
            new_tile(xc,yc,False)
            tiles[(xc,yc)]["sides"][1],tiles[(xc,yc)]["sides"][2] = self.TILE_N,self.TILE_W
                
    def score(self, tilex, tiley):
        if (tilex, tiley) not in self.tiles:
            return -99
        
        score = 0
        tile = self.tiles[(tilex, tiley)]
        if tile["visited"]:
            score -= 10
        score += sum(tile["sides"])
        return score

def main():
    rclpy.init()
    node = Control()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()