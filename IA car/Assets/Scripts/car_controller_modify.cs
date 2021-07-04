using System;
using UnityEngine;
using UnityStandardAssets.CrossPlatformInput;

using System.Collections;
using System.Net;
using System.Net.Sockets;


namespace UnityStandardAssets.Vehicles.Car
{
	[RequireComponent(typeof (CarController))]
	public class car_controller_modify : MonoBehaviour {

		private Socket _clientSocket = new Socket(AddressFamily.InterNetwork,SocketType.Stream,ProtocolType.Tcp);
		private byte[] _recieveBuffer = new byte[8142];

		private CarController m_Car; // the car controller we want to use
		private Rigidbody rb;
		private Vector3 vel;
		private Quaternion rotationAll;

		public GetDead captorDead;

		public CubeCaptor captorCubeFirstRight;
		public CubeCaptor captorCubeFirstFront;
		public CubeCaptor captorCubeFirstLeft;
		public CubeCaptor captorCubeSecondRight;
		public CubeCaptor captorCubeSecondFront;
		public CubeCaptor captorCubeSecondLeft;

		public float rotationOfMyCar = 0f;
		public float avanceOfMyCar = 0f;

		private int lastEffectKillTheCar = 0;
		private bool respawn = false;
		private Vector3 start_pos = Vector3.zero;//= gameObject.transform.position;//
		private Quaternion start_rot;
		//private Vector3 start_rot = Vector3.zero;
		//private float start_pos_x = 0f;//;transform.position.x;
		//private float start_pos_y = 0f;//;transform.position.y;
		//private float start_pos_z = 0f;//;transform.position.z;

		void Start() {
			start_pos = gameObject.transform.position;
			start_rot = gameObject.transform.rotation;
			//start_pos_x = transform.position.x;
			//start_pos_y = transform.position.y;
			//start_pos_z = transform.position.z;
			//PlayerPrefs.SetFloat("CarX", transform.position.x);
			//PlayerPrefs.SetFloat("CarY", transform.position.y);
			//PlayerPrefs.SetFloat("CarZ", transform.position.z);
			SetupServer();
		}

		void Update() {
			vel = rb.velocity;
			rotationAll = transform.rotation;
			if (respawn == true) {
				transform.position = start_pos;
				rb.velocity = new Vector3 (0, 0, 0);
				transform.rotation  = Quaternion.identity;//= start_rot;
				StartCoroutine(WaitSomeTime());
				rb.velocity = new Vector3 (0, 0, 0);
				transform.rotation  = Quaternion.identity;//= start_rot;
				StartCoroutine(WaitSomeTime());
				rb.velocity = new Vector3 (0, 0, 0);
				transform.rotation  = Quaternion.identity;//= start_rot;
				respawn = false;
			}
		}

		IEnumerator WaitSomeTime()
		{
			yield return new WaitForSeconds(2);
		}
		
		private void Awake()
		{
			// get the car controller
			m_Car = GetComponent<CarController>();
			rb = gameObject.GetComponent<Rigidbody>();
		}

		private void FixedUpdate()
		{
			// pass the input to the car!
			//float h = CrossPlatformInputManager.GetAxis("Horizontal");//-1 and 0 and 1
			float h = rotationOfMyCar;
			//float v = CrossPlatformInputManager.GetAxis("Vertical"); // between -1 and 0 and 1
			float v = avanceOfMyCar;
			#if !MOBILE_INPUT
			float handbrake = CrossPlatformInputManager.GetAxis("Jump");
			m_Car.Move(h, v, v, handbrake);
			#else
			m_Car.Move(h, v, v, 0f);
			#endif
		}

		void OnApplicationQuit()
		{
			_clientSocket.Close ();
		}

		private void SetupServer()
		{
			try
			{
				_clientSocket.Connect(new IPEndPoint(IPAddress.Loopback,50000));
			}
			catch(SocketException ex)
			{
				Debug.Log(ex.Message);
			}

			_clientSocket.BeginReceive(_recieveBuffer,0,_recieveBuffer.Length,SocketFlags.None,new AsyncCallback(ReceiveCallback),null);

		}


		private void ReceiveCallback(IAsyncResult AR)
		{
			//Check how much bytes are recieved and call EndRecieve to finalize handshake
			int recieved = _clientSocket.EndReceive(AR);

			if(recieved <= 0)
				return;

			//Copy the recieved data into new buffer , to avoid null bytes
			byte[] recData = new byte[recieved];
			Buffer.BlockCopy(_recieveBuffer,0,recData,0,recieved);

			//Process data here the way you want , all your bytes will be stored in my data
			string my_data_str = System.Text.Encoding.Default.GetString (_recieveBuffer);
			//Debug.Log(my_data);
			string[] my_data_split_str = my_data_str.Split('#');
			if(my_data_split_str[0] == "127" && my_data_split_str[1] == "127"){
				respawn = true;
				my_data_split_str [0] = "0";
				my_data_split_str [1] = "0";
				//gameObject.transform.position = new Vector3 (start_pos_x, start_pos_y, start_pos_z);//start_pos;
				//transform.position = new Vector3(PlayerPrefs.GetFloat("CarX"),PlayerPrefs.GetFloat("CarY"),PlayerPrefs.GetFloat("CarZ"));
			}
			if (respawn == false) {
				//int rotationOfDesired;
				//int.TryParse (my_data_split_str[0], out rotationOfDesired);
				//rotationOfMyCar = rotationOfDesired;
				rotationOfMyCar = float.Parse (my_data_split_str [0]);

				//int vitesseAvance;
				//int.TryParse (my_data_split_str[1], out vitesseAvance);
				//avanceOfMyCar = vitesseAvance;
				avanceOfMyCar = float.Parse (my_data_split_str [1]);
				Debug.Log(avanceOfMyCar);
				Debug.Log(rotationOfMyCar);
				lastEffectKillTheCar = captorDead.isDead;
				string message = lastEffectKillTheCar.ToString () + "#" + vel.magnitude.ToString () + "#" + rotationAll.y + "#" + captorCubeFirstRight.touchWall.ToString () + "#" + captorCubeFirstFront.touchWall.ToString () + "#" + captorCubeFirstLeft.touchWall.ToString () + "#" + captorCubeSecondRight.touchWall.ToString () + "#" + captorCubeSecondFront.touchWall.ToString () + "#" + captorCubeSecondLeft.touchWall.ToString ();

				SendData (System.Text.Encoding.Default.GetBytes (message));

				//Start receiving again
				_clientSocket.BeginReceive (_recieveBuffer, 0, _recieveBuffer.Length, SocketFlags.None, new AsyncCallback (ReceiveCallback), null);
			} else {
				rotationOfMyCar = float.Parse (my_data_split_str [0]);
				avanceOfMyCar = float.Parse (my_data_split_str [1]);

				string message = "0#0#0#0#0#0#0#0#0";
				SendData (System.Text.Encoding.Default.GetBytes (message));

				//Start receiving again
				_clientSocket.BeginReceive (_recieveBuffer, 0, _recieveBuffer.Length, SocketFlags.None, new AsyncCallback (ReceiveCallback), null);
			}
		}

		private void SendData(byte[] data)
		{
			SocketAsyncEventArgs socketAsyncData = new SocketAsyncEventArgs();
			socketAsyncData.SetBuffer(data,0,data.Length);
			_clientSocket.SendAsync(socketAsyncData);
		}
	}
}