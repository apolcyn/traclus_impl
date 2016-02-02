package boliu;

import java.io.OutputStream;
import java.util.ArrayList;

public class Cluster {
	
	private int m_clusterId;		// the identifier of this cluster
	private int m_nDimensions;		// the dimensionality of this cluster
	private int m_nTrajectories;	// the number of trajectories belonging to this cluster
	private int m_nPoints;			// the number of points constituting a cluster 
	private ArrayList<CMDPoint> m_pointArray;	// the array of the cluster points

	public Cluster() {	
		
		m_clusterId = -1;
		m_nDimensions = 2;
		m_nTrajectories = 0;
		m_nPoints = 0;
		m_pointArray = new ArrayList<CMDPoint>();
	}
	
	public Cluster(int id, int nDimensions) {		
		
		m_clusterId = id;
		m_nDimensions = nDimensions;
		m_nTrajectories = 0;
		m_nPoints = 0;
		m_pointArray = new ArrayList<CMDPoint>();
	}
	
	public void setM_clusterId(int m_clusterId) {
		this.m_clusterId = m_clusterId;
	}
	
	public int getM_clusterId() {
		return m_clusterId;
	}
	
	/**
	 * set m_nTrajectories --the number of trajectories belonging to this cluster
	 * @param density
	 */
	public void setDensity(int density) {
		this.m_nTrajectories = density;
	}
	/**
	 * get the density -- the number of trajectories belonging to this cluster
	 * @return density number
	 */
	public int getDensity() {
		return this.m_nTrajectories;
	}
	
	public void addPointToArray(CMDPoint point) {
		
		m_pointArray.add(point);
		m_nPoints++;				
	}
	
	public ArrayList<CMDPoint> getM_PointArray( ) {
		return this.m_pointArray;
	}
	
	public boolean writeCluster(OutputStream outfile) {
						
		return true;
		
	}
	
	
	
	
	

	
}
