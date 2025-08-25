import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { api, setAuthToken } from './api'

interface AuthContextValue {
	token: string | null
	login: (username: string, password: string) => Promise<void>
	logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

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

	const value = useMemo(() => ({ token, login, logout }), [token])
	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
	const ctx = useContext(AuthContext)
	if (!ctx) throw new Error('useAuth must be used within AuthProvider')
	return ctx
}

export const RequireAuth: React.FC = () => {
	const { token } = useAuth()
	if (!token) return <Navigate to="/login" replace />
	return <Outlet />
}