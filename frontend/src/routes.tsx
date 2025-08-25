import React, { useEffect, useState } from 'react'
import { api } from './api'
import { Bar } from 'react-chartjs-2'
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	BarElement,
	Title,
	Tooltip,
	Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export const Home: React.FC = () => <div>Welcome to BCM-MAP</div>

export const Assessments: React.FC = () => {
	const [items, setItems] = useState<any[]>([])
	useEffect(() => {
		api.get('/assessments/').then(r => setItems(r.data.results || r.data))
	}, [])
	return (
		<div>
			<h3>Assessments</h3>
			<ul>
				{items.map(it => (
					<li key={it.id}>{it.title} — status: {it.status}</li>
				))}
			</ul>
		</div>
	)
}

export const Dashboard: React.FC = () => {
	const [items, setItems] = useState<any[]>([])
	useEffect(() => {
		api.get('/assessments/').then(r => setItems(r.data.results || r.data))
	}, [])
	const labels = items.map((it: any) => it.title)
	const data = {
		labels,
		datasets: [
			{
				label: 'Overall Score',
				data: items.map((it: any) => it.overall_score ?? 0),
				backgroundColor: 'rgba(53, 162, 235, 0.5)',
			},
		],
	}
	return (
		<div>
			<h3>Dashboard</h3>
			<Bar data={data} />
		</div>
	)
}

export const AssessmentForm: React.FC<{ assessmentId: number }> = ({ assessmentId }) => {
	const [responses, setResponses] = useState<any[]>([])
	const [questions, setQuestions] = useState<any[]>([])
	useEffect(() => {
		Promise.all([
			api.get('/questions/').then(r => setQuestions(r.data.results || r.data)),
			api.get(`/responses/?assessment=${assessmentId}`).then(r => setResponses(r.data.results || r.data)),
		])
	}, [assessmentId])

	const upsertResponse = async (questionId: number, rating: number, comment: string) => {
		let existing = responses.find(r => r.question === questionId)
		if (existing) {
			const res = await api.patch(`/responses/${existing.id}/`, { rating, comment })
			setResponses(rs => rs.map(r => (r.id === existing.id ? res.data : r)))
		} else {
			const res = await api.post('/responses/', { assessment: assessmentId, question: questionId, rating, comment })
			setResponses(rs => [...rs, res.data])
		}
	}

	useEffect(() => {
		const id = setInterval(async () => {
			for (const r of responses) {
				if (r.id) {
					await api.patch(`/responses/${r.id}/`, { rating: r.rating, comment: r.comment })
				}
			}
		}, 30000)
		return () => clearInterval(id)
	}, [responses])

	const uploadEvidence = async (responseId: number, file: File) => {
		const form = new FormData()
		form.append('response', String(responseId))
		form.append('file', file)
		await api.post('/evidence/', form, { headers: { 'Content-Type': 'multipart/form-data' } })
	}

	return (
		<div>
			{questions.map((q: any) => {
				const resp = responses.find(r => r.question === q.id)
				return (
					<div key={q.id} style={{ marginBottom: 16 }}>
						<div>{q.text}</div>
						<input type="number" min={0} max={5} value={resp?.rating ?? ''}
							onChange={e => upsertResponse(q.id, Number(e.target.value), resp?.comment || '')} />
						<textarea placeholder="Comment" value={resp?.comment ?? ''}
							onChange={e => upsertResponse(q.id, resp?.rating ?? 0, e.target.value)} />
						{resp && (
							<input type="file" accept="application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
								onChange={e => e.target.files && uploadEvidence(resp.id, e.target.files[0])} />
						)}
					</div>
				)
			})}
		</div>
	)
}