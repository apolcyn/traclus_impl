package boliu;

public class CMDPoint {
	
	
	private int m_nDimensions; 	// the number of dimensions of a point
	double[] m_coordinate;	    // the coordinate of a point
	
	//default constructor which shall be never used, we can use the following constructor instead
	public CMDPoint() {		
		m_nDimensions = 2;
		m_coordinate = new double[m_nDimensions];
		m_coordinate[0] = m_coordinate[1] = 0.0;
	}
	
	public CMDPoint(int nDimensions) {
		
		m_nDimensions = nDimensions;
		m_coordinate = new double[m_nDimensions];
		for( int i=0; i < m_nDimensions; i++ ) {
			m_coordinate[i] = 0.0;
		}
		
	}
	
	/**
	 * return the coordinate according to the dimension 'nth'
	 * @param nth #dimension
	 * @return
	 */
	public double getM_coordinate(int nth) {
		
		return m_coordinate[nth];
	}
	
	public int getM_nDimensions() {
		return m_nDimensions;
	}
	
	/**
	 * set the coordinate according to the dimension
	 * @param nth dimension
	 * @param value value
	 */
	public void setM_coordinate(int nth, double value) {
		this.m_coordinate[nth] = value;
	}
	
	
}
