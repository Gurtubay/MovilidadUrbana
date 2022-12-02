// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

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
public class StateData
{
    public string id;
    public string state;
    public float x, y, z;
    public StateData(string id, string state, float x, float y, float z)
    {
        this.id = id;
        this.state = state;
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

public class StatesData
{
    public List<StateData> states;

    public StatesData() => this.states = new List<StateData>();
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getStates = "/getStates";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;
    StatesData statesData;
    Dictionary<string, GameObject> agents;
    Dictionary<string, GameObject> semaforo;
    Dictionary<string, Vector3> prevPositions, currPositions;
    Dictionary<string, string> colores;

    bool updated = false, started = false;

    public GameObject agentPrefab, floor, semaforoPrefab;
    public int NAgents;
    public float timeToUpdate = 1.0f;
    private float timer, dt;


    void Start()
    {
        agentsData = new AgentsData();
        statesData = new StatesData();
        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        semaforo = new Dictionary<string, GameObject>();
        colores = new Dictionary<string, string>();

        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }
            foreach(var color in colores)
            {
               if (color.Value == "yellow")
                {
                    semaforo[color.Key].GetComponent<Renderer>().materials[0].color = Color.yellow;
                }
               if (color.Value == "green")
               {
                   semaforo[color.Key].GetComponent<Renderer>().materials[0].color = Color.green;
               }
                if (color.Value == "red")
                {
                    semaforo[color.Key].GetComponent<Renderer>().materials[0].color = Color.red;
                }
            }
        
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
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetStates());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        

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
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetAgentsData());
            Debug.Log("Getting States");
            StartCoroutine(GetStates());

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

            foreach(AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y-1, agent.z);

                    if(!started)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;
                    }
            }

           
        }
    }
    
    IEnumerator GetStates() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getStates);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            statesData = JsonUtility.FromJson<StatesData>(www.downloadHandler.text);

            foreach (StateData agent in statesData.states)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y-1, agent.z);

                if (!started)
                {
                    semaforo[agent.id] = Instantiate(semaforoPrefab, newAgentPosition, Quaternion.identity);
                }
                else
                {
                    colores[agent.id] = agent.state;
                }
            }
        }
        updated = true;
        if (!started) started = true;
    }
    
    
}
