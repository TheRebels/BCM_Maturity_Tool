import { createContext, useContext } from 'react'

export interface AuthContextValue {
	token: string | null
	login: (username: string, password: string) => Promise<void>
	logout: () => void
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export const useAuth = () => {
	const ctx = useContext(AuthContext)
	if (!ctx) throw new Error('useAuth must be used within AuthProvider')
	return ctx
}

