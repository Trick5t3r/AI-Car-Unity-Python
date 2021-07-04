using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeCaptor : MonoBehaviour {

	public int touchWall = 0;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
	}

	void OnTriggerEnter(Collider other) {
		if (other.gameObject.tag == "wall") {
			touchWall = 1;
		}
	}

	void OnTriggerStay(Collider other) {
		if (other.gameObject.tag == "wall") {
			touchWall = 1;
		}
	}

	void OnTriggerExit(Collider other) {
		if (other.gameObject.tag == "wall") {
			touchWall = 0;
		}
	}
}
