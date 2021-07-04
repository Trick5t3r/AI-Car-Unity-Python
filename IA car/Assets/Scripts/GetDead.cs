using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetDead : MonoBehaviour {

	public int isDead = 0;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	void OnTriggerEnter(Collider other) {
		if (other.gameObject.tag == "wall") {
			isDead = 1;
		}
	}

	void OnTriggerStay(Collider other) {
		if (other.gameObject.tag == "wall") {
			isDead = 1;
		}
	}
	void OnTriggerExit(Collider other) {
		if (other.gameObject.tag == "wall") {
			isDead = 0;
		}
	}
}
