using UnityEngine;
using System.Collections;
using System;
using System.Net;
using System.Net.Sockets;

public class networkSocketSO : MonoBehaviour {

	private Socket _clientSocket = new Socket(AddressFamily.InterNetwork,SocketType.Stream,ProtocolType.Tcp);
	private byte[] _recieveBuffer = new byte[8142];

	public Transform car;

	public float rotatieY;

	void Start() {
		SetupServer ();
	}

	void Update() {

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
		string my_data = System.Text.Encoding.Default.GetString (_recieveBuffer);
		Debug.Log(my_data);
		SendData (System.Text.Encoding.Default.GetBytes ("ping"));

		//Start receiving again
		_clientSocket.BeginReceive(_recieveBuffer,0,_recieveBuffer.Length,SocketFlags.None,new AsyncCallback(ReceiveCallback),null);
	}

	private void SendData(byte[] data)
	{
		SocketAsyncEventArgs socketAsyncData = new SocketAsyncEventArgs();
		socketAsyncData.SetBuffer(data,0,data.Length);
		_clientSocket.SendAsync(socketAsyncData);
	}
}