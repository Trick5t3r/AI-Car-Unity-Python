using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetDeadCollider : MonoBehaviour {

	public int isDead = 0;

	// Use this for initialization
	void Start () {

	}

	// Update is called once per frame
	void Update () {

	}

	void OnCollisionEnter(Collision other) {
		if (other.gameObject.tag == "wall") {
			isDead = 1;
			Debug.Log (isDead);
		}
		Debug.Log (other);
	}

	void OnCollisionStay(Collision other) {
		if (other.gameObject.tag == "wall") {
			isDead = 1;
		}
	}
}