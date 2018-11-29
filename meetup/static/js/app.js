new Vue({
	el: "#app",
	data: {
		meetups: [],
		syncing: [],
		syncErrors: [],
		meetupUrl: "",
		intervalId: null,
	},
	methods: {
		isSyncing(meetup) {
			return this.syncing.indexOf(meetup.id) != -1;
		},
		hasSyncError(meetup) {
			return this.syncErrors.indexOf(meetup.id) != -1;
		},
		loadContext() {
			const context = JSON.parse(document.getElementById("vue-context").textContent);
			this.meetups = context.meetups;
		},
		isSyncing(meetup) {
			const options = {
				method: "GET",
				headers: new Headers({
					"Content-Type": "application/json",
				})
			}

			fetch(`/api/meetups/${meetup.id}/`, options)
				.then(response => {
					return response.json()
				})
				.then(data => {
					if (meetup.syncing == data.syncing) {
						this.syncing.splice(this.syncing.indexOf(meetup.id), 1);
					}

					meetup.syncing = data.syncing;

					if (this.syncing.length == 0) {
						this.intervalId = null;
					}
				})
		},
		updateMeetups() {
			this.syncing.forEach(meetup_id => {
				const meetup = this.meetups.filter(meetup => {
					return meetup.id == meetup_id;
				})

				this.isSyncing(meetup[0]);
			});
		},
		addNewMeetup() {

		},
		syncMeetup(meetup) {
			this.syncing.push(meetup.id);
			this.syncErrors.splice(this.syncErrors.indexOf(meetup.id), 1);

			const payload = {"meetup_id": meetup.id};
			const options = {
				method: "POST",
				body: JSON.stringify(payload),
				headers: new Headers({
					"Content-Type": "application/json",
				})
			}

			fetch("/api/sync-meetup/", options)
				.then(response => {
					return response.json();
				})
				.then(data => {
					meetup.syncing = data.syncing;
					if (this.intervalId == null) {
						this.intervalId = setInterval(this.updateMeetups, 2000);
					}
				})
				.catch(error => {
					this.syncing.splice(this.syncing.indexOf(meetup.id), 1);
					this.syncErrors.push(meetup.id);
				});
		}
	},
	mounted() {
		this.loadContext();
	}
});