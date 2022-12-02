using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficLight : MonoBehaviour
{
    public GameObject luz;
    public Transform posVerde;
    public Transform posAmarilla;
    public Transform posRoja;

    private string roja;
    private string amarilloDesdeRoja;
    private string amarilloDesdeVerde;
    private string verde;

    void Start()
    {
        verde = "verde";
    }

    void Update()
    {
        if (verde == "verde"){
            luz.transform.position = posVerde.position;
            luz.GetComponent<Light>().color = Color.green;
            StartCoroutine(luzVerde());
            amarilloDesdeRoja = "";
        }
        
        
        if (amarilloDesdeVerde=="amarilloDesdeVerde"){
            
            luz.transform.position = posAmarilla.position;
            luz.GetComponent<Light>().color = Color.yellow;
            StartCoroutine(luzAmarilloV());
            verde = "";
        }

        if (amarilloDesdeRoja=="amarilloDesdeRoja"){
            luz.transform.position = posAmarilla.position;
            luz.GetComponent<Light>().color = Color.yellow;
            StartCoroutine(luzAmarilloR());
            roja = "";
        }
        if (roja == "roja"){
            luz.transform.position = posRoja.position;
            luz.GetComponent<Light>().color = Color.red;
            StartCoroutine(luzRoja());
            amarilloDesdeVerde = "";
        }
        
    }
    IEnumerator luzVerde()
    {
        yield return new WaitForSeconds(10);
        amarilloDesdeVerde = "amarilloDesdeVerde";
    }
    IEnumerator luzAmarilloV()
    {
        yield return new WaitForSeconds(3);
        roja = "roja";
    }
    IEnumerator luzAmarilloR()
    {
        yield return new WaitForSeconds(3);
        verde = "verde";
    }
    IEnumerator luzRoja()
    {
        yield return new WaitForSeconds(10);
        amarilloDesdeRoja = "amarilloDesdeRoja";
    }
}

