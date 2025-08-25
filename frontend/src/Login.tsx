import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from './auth'

const Login: React.FC = () => {
	const { login } = useAuth()
	const nav = useNavigate()
	const [username, setUsername] = useState('admin')
	const [password, setPassword] = useState('admin123')
	const [error, setError] = useState<string | null>(null)

	const onSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		try {
			await login(username, password)
			nav('/')
		} catch (err: any) {
			setError('Login failed')
		}
	}

	return (
		<form onSubmit={onSubmit} style={{ maxWidth: 320, margin: '48px auto', display: 'grid', gap: 12 }}>
			<h3>Login</h3>
			<input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
			<input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
			{error && <div style={{ color: 'red' }}>{error}</div>}
			<button type="submit">Sign in</button>
		</form>
	)
}

export default Login