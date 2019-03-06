new Vue({
	el: "#app",
	name: "SyncMeetup",
	data: {
		meetups: [],
		syncing: [],
		syncErrors: [],
		meetupUrl: "",
		intervalId: null,
    isAdding: false,
	},
	methods: {
    /*
     * Check if a meetup is syncing.
     */
		isSyncing(meetup) {
			return this.syncing.indexOf(meetup.id) != -1;
		},
    /*
     * Check if a meetup sync errored.
     */
		hasSyncError(meetup) {
			return this.syncErrors.indexOf(meetup.id) != -1;
		},
    /*
     * Load the context from the server.
     */
		loadContext() {
			const context = JSON.parse(document.getElementById("vue-context").textContent);
			this.meetups = context.meetups;
		},
    /*
     * Update meetup data.
     */
		updateMeetups() {
      const options = {
        method: "GET",
      }

      fetch("/api/meetups/", options)
        .then(resp => {
          return resp.json();
        })
        .then(data => {
          this.meetups = data;
          this.syncing.forEach(meetup_id => {
            const meetup = this.meetups.filter(meetup => {
              return meetup.id == meetup_id;
            })

            this.isSyncing(meetup[0]);
          });
        });
		},
    /*
     * Add a new meetup.
     */
		addNewMeetup() {
      const options = {
        method: "POST",
        body: JSON.stringify({
          name: this.meetupUrl,
          syncing: false,
        }),
        headers: new Headers({
          "Content-Type": "application/json"
        })
      }

      this.isAdding = true;

      fetch("/api/meetups/", options)
        .then(resp => {
          return resp.json();
        })
        .then(meetup => {
          this.meetups.push(meetup);
          this.isAdding = false;
          this.meetupUrl = null;
        })
        .catch(error => {
          console.log(error)
          this.isAdding = false;
        });
		},
    /*
     * Sync a meetup.
     */
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
