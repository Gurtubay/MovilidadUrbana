
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;

    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]
public class BoxData
{
    public string id;
    public float x, y, z;

    public BoxData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]
public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

[Serializable]
public class Rem
{
    public String message;

}

[Serializable]
public class BoxesData
{
    public List<BoxData> positions;

    public BoxesData() => this.positions = new List<BoxData>();
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    
    //string getObstaclesEndpoint = "/getObstacles";
    string getBoxEndpoint = "/getBoxes";//--> cambios
    
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;//--> cambios 211
    BoxesData boxesData;
    Rem orden;
    Dictionary<string, GameObject> agents;
    //Dictionary<string, GameObject> boxes;
    Dictionary<string, Vector3> prevPositions, currPositions;
    //Dictionary<string, Vector3> boxInicial, boxFinal;

    bool updatedBoxes = false, startedBoxes = false;
    bool updatedAgents = false, startedAgents = false;

    public GameObject agentPrefab, floor, BoxPrefab;//--> cambios
    public int NAgents, width, height, XBox;//-->cambios
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        //cambios
        boxesData = new BoxesData();//--> cambios
       // boxInicial = new Dictionary<string, Vector3>();
       // boxFinal = new Dictionary<string, Vector3>();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        //boxes = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width / 1, 1, (float)height / 1);
        floor.transform.localPosition = new Vector3((float)width / 1 , 1, (float)height / 1 );

        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update()
    {
        if (timer < 0)
        {
            timer = timeToUpdate;
            updatedAgents = false;
            updatedBoxes = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updatedAgents && updatedBoxes)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach (var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if (direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);

            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            Debug.Log(www.downloadHandler.text);
            orden = JsonUtility.FromJson<Rem>(www.downloadHandler.text);
            if (orden.message == "666"){
                UnityEditor.EditorApplication.isPlaying = false;
            }
            else
            { 
                StartCoroutine(GetAgentsData());
                StartCoroutine(GetBoxData());
            }
           
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        //cambio
        form.AddField("XBox", XBox.ToString());
        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            StartCoroutine(GetAgentsData());
            Debug.Log("Getting Agents positions");
            //StartCoroutine(GetObstacleData());
            //cambios
            StartCoroutine(GetBoxData());
        }
    }

    IEnumerator GetAgentsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach (AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                //Console.WriteLine(agent.positions);

                if (!startedAgents)
                {
                    prevPositions[agent.id] = newAgentPosition;
                    agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                }
                else
                {
                    Vector3 currentPosition = new Vector3();
                    if (currPositions.TryGetValue(agent.id, out currentPosition))
                        prevPositions[agent.id] = currentPosition;
                    currPositions[agent.id] = newAgentPosition;
                }
            }
            //XBox.transform.parent = robot.transform
            updatedAgents = true;
            if (!startedAgents) startedAgents = true;
        }
    }
    IEnumerator GetBoxData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBoxEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            boxesData = JsonUtility.FromJson<BoxesData>(www.downloadHandler.text);

            foreach (BoxData agent in boxesData.positions)
            {
                Vector3 newBoxPosition = new Vector3(agent.x, agent.y, agent.z);

                if (!startedBoxes)
                {
                    prevPositions[agent.id] = newBoxPosition;
                    agents[agent.id] = Instantiate(BoxPrefab, newBoxPosition, Quaternion.identity);
                }
                else
                {
                    Vector3 currentPosition = new Vector3();
                    if (currPositions.TryGetValue(agent.id, out currentPosition))
                        prevPositions[agent.id] = currentPosition;
                    currPositions[agent.id] = newBoxPosition;
                }
            }
            //XBox.transform.parent = robot.transform
            updatedBoxes = true;
            if (!startedBoxes) startedBoxes = true;
                
        }   
    }
/*
    IEnumerator GetObstacleData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            obstacleData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(obstacleData.positions);

            foreach (AgentData obstacle in obstacleData.positions)
            {
                Instantiate(obstaclePrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
            }
        }
    }
  */ /* 
    IEnumerator GetBoxData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBoxEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            BoxData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(BoxData.positions);

            foreach (AgentData Box in BoxData.positions)
            {
                Vector3 newBoxPosition = new Vector3(Box.x, Box.y, Box.z);

                Instantiate(BoxPrefab, newBoxPosition, Quaternion.identity);
            }
        }
    }
 */

}
