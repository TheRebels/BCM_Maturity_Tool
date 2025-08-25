import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App.tsx'
import { Home, Assessments, Dashboard } from './routes.tsx'
import Login from './Login'
import { AuthProvider, RequireAuth } from './auth'
import './index.css'

const queryClient = new QueryClient()

const router = createBrowserRouter([
	{ path: '/login', element: <Login /> },
	{
		path: '/',
		element: <App />,
		children: [
			{ index: true, element: <Home /> },
			{ element: <RequireAuth />,
				children: [
					{ path: 'assessments', element: <Assessments /> },
					{ path: 'dashboard', element: <Dashboard /> },
				],
			},
		],
	},
])

ReactDOM.createRoot(document.getElementById('root')!).render(
	<React.StrictMode>
		<QueryClientProvider client={queryClient}>
			<AuthProvider>
				<RouterProvider router={router} />
			</AuthProvider>
		</QueryClientProvider>
	</React.StrictMode>,
)
