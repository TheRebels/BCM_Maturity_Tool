import { Link, Outlet } from 'react-router-dom'

export default function App() {
	return (
		<div style={{ padding: 16 }}>
			<header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
				<h2>BCM-MAP</h2>
				<nav style={{ display: 'flex', gap: 12 }}>
					<Link to="/">Home</Link>
					<Link to="/assessments">Assessments</Link>
					<Link to="/dashboard">Dashboard</Link>
				</nav>
			</header>
			<main>
				<Outlet />
			</main>
		</div>
	)
}
