#r "Newtonsoft.Json"
#r "Microsoft.WindowsAzure.Storage"
using System;
using Newtonsoft.Json.Linq;
using Microsoft.WindowsAzure.Storage.Table;



public static void Run(string myIoTHubMessage, CloudTable outputTable, TraceWriter log)
{
    

    log.Info(myIoTHubMessage);

    try
    {
        //var st = "{\"cursor_position\": 1, \"command\" : \"command 0\", \"robot_time\": \"2019-06-04T14:07:03.921000\"}";
        //log.Info(" ");
        //log.Info(st);
        Grasshopper grasshopper = new Grasshopper();
        var message = JObject.Parse(myIoTHubMessage);

        grasshopper.PartitionKey = "grasshopper";
        grasshopper.RowKey = DateTime.Now.ToString("hh.mm.ss.ffffff");

        grasshopper.cursor_position  = message["cursor_position"].ToString();
         
        grasshopper.command = message["command"].ToString();
        grasshopper.robot_time  = message["robot_time"].ToString();
        log.Info(grasshopper.robot_time);

        {
            var operation = TableOperation.Insert(grasshopper);
            outputTable.ExecuteAsync(operation);
            log.Info($"Write Sucessfull");
        }

    }

    catch (Exception ex)
    {
        log.Info("Exception  is  =  " + ex.Message);
        return;
    }



}

class Grasshopper : TableEntity
{

    public string cursor_position { get; set; }
    public string command { get; set; }
    public string robot_time { get; set; }

}


//System.DateTime dtDateTime = new DateTime(1970,1,1,0,0,0,0,System.DateTimeKind.Utc);
//dtDateTime = dtDateTime.AddSeconds( unixTimeStamp ).ToLocalTime();
