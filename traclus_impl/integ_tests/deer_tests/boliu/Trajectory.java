package boliu;

import java.util.ArrayList;

public class Trajectory {	
	
	private int m_trajectoryId;		// the identifier of this trajectory
	private int m_nDimensions;		// the dimensionality of this trajectory
	private int m_nPoints;			// the number of points constituting a trajectory 
	private ArrayList<CMDPoint> m_pointArray;	// the array of the trajectory points
	private int m_nPartitionPoints;		// the number of partition points in a trajectory
	private ArrayList<CMDPoint> m_partitionPointArray;	// the array of the partition points
	
	
	public Trajectory() {
		
		m_trajectoryId = -1;
		m_nDimensions = 2;
		m_nPoints = 0;
		m_nPartitionPoints = 0;
		m_pointArray = new ArrayList<CMDPoint>();
		m_partitionPointArray = new ArrayList<CMDPoint>();
		
	}
	
	public Trajectory(int id, int nDimensions) {
	
		m_trajectoryId = id;
		m_nDimensions = nDimensions;
		m_nPoints = 0;
		m_nPartitionPoints = 0;
		m_pointArray = new ArrayList<CMDPoint>();
		m_partitionPointArray = new ArrayList<CMDPoint>();
	}
//two methods	
	public void addPointToArray(CMDPoint point) {
		
		m_pointArray.add(point);
		m_nPoints++;
		
	}
	
	public void addPartitionPointToArray(CMDPoint point) {
		
		m_partitionPointArray.add(point);		
		m_nPartitionPoints++;
		
	}
	
	public void setM_trajectoryId(int id) {
		this.m_trajectoryId = id;
	}
	
	public int getM_trajectoryId() {
		return m_trajectoryId;
	}						
	
	public int getM_nDimensions() {
		return m_nDimensions;
	}

	public void setM_nDimensions(int m_nDimensions) {
		this.m_nDimensions = m_nDimensions;
	}

	public int getM_nPoints() {
		return m_nPoints;
	}

	public void setM_nPoints(int m_nPoints) {
		this.m_nPoints = m_nPoints;
	}

	public ArrayList<CMDPoint> getM_pointArray() {
		return m_pointArray;
	}

	public void setM_pointArray(ArrayList<CMDPoint> m_pointArray) {
		this.m_pointArray = m_pointArray;
	}

	public int getM_nPartitionPoints() {
		return m_nPartitionPoints;
	}

	public void setM_nPartitionPoints(int m_nPartitionPoints) {
		this.m_nPartitionPoints = m_nPartitionPoints;
	}

	public ArrayList<CMDPoint> getM_partitionPointArray() {
		return m_partitionPointArray;
	}

	public void setM_partitionPointArray(ArrayList<CMDPoint> m_partitionPointArray) {
		this.m_partitionPointArray = m_partitionPointArray;
	}


 
}
