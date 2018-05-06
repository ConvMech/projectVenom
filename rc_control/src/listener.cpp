#include "ros/ros.h"
#include "mavros_msgs/RCIn.h"
#include "std_msgs/String.h"
#include <sstream>

class SubscribeAndPublish{
public:
  int old_flag;
  SubscribeAndPublish(){
    pub_ = n_.advertise<std_msgs::String>("chatter", 1000);
    sub_ = n_.subscribe("/mavros/rc/in", 10000,&SubscribeAndPublish::callback, this);
  }
  void callback(const mavros_msgs::RCIn& msg){
    std_msgs::String output; output.data = "record";
    std_msgs::String output_;output_.data = "stop";
    std_msgs::String output_cam;output_cam.data = "record_cam";
     if(msg.channels[5] > 1500 && msg.channels[7] >  1200 && msg.channels[7] < 1700){
      //ROS_INFO("record_ON");
      // ROS_INFO(msg.channels[7]); 
       if (old_flag == 0){
          pub_.publish(output); old_flag = 1;
       }
     }
     else if(msg.channels[5] > 1500 && msg.channels[7] > 1700){
      //ROS_INFO("record_ON");
       if (old_flag == 0){
          pub_.publish(output_cam); old_flag = 1;
       }
     }
     else{
       //ROS_INFO("record_OFF");
       if (old_flag == 1){
          pub_.publish(output_); old_flag = 0;
       }
     }
   }
private:
  ros::NodeHandle n_; 
  ros::Publisher pub_;
  ros::Subscriber sub_;
};

int main(int argc, char **argv)
{
  //Initiate ROS
  ros::init(argc, argv, "subscribe_and_publish");
  //Create an object of class SubscribeAndPublish that will take care of everything
  SubscribeAndPublish SAPObject;
  SAPObject.old_flag = 0;
  ros::spin();
  return 0;
}

/*
void callback_RC_takeover(const mavros_msgs::RCIn& msg);
 
int main(int argc, char **argv){
    ros::init(argc, argv, "rc_data");
    ros::NodeHandle n;
    ROS_INFO("started_rc_listener, listening to channel 8");
    ros::Subscriber rc_in = n.subscribe("/mavros/rc/in", 10000, &callback_RC_takeover);
    ros::spin();
    ROS_INFO("ending_rc!");
    return 0;
}

void callback_RC_takeover(const mavros_msgs::RCIn& msg)
{
   // ROS_INFO("Safety: %d ",msg.channels[7]);
   if(msg.channels[5] > 1500){
       ROS_INFO("record_ON");
   }else{
       ROS_INFO("record_OFF");
   }
}
*/
