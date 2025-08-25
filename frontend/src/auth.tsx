import React, { useEffect, useMemo, useState } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { api, setAuthToken } from './api'
import { AuthContext, useAuth, type AuthContextValue } from './auth-context'

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))

	useEffect(() => {
		setAuthToken(token)
		if (token) localStorage.setItem('token', token)
		else localStorage.removeItem('token')
	}, [token])

	const login = async (username: string, password: string) => {
		const res = await api.post('/auth/token/', { username, password })
		setToken(res.data.access)
	}

	const logout = () => setToken(null)

	const value: AuthContextValue = useMemo(() => ({ token, login, logout }), [token])
	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const RequireAuth: React.FC = () => {
	const { token } = useAuth()
	if (!token) return <Navigate to="/login" replace />
	return <Outlet />
}