<template>
    <md-layout md-flex="100">
        <md-card>
                <h3>{{topic}} Badges</h3>
                <md-layout v-for="badge in availableBadges"
                        :key="badge.key"
                        md-flex="33"
                        class="badgeGutter"
                        md-gutter>
                    <user-badge :badge="badge"></user-badge>
                </md-layout>
        </md-card>
    </md-layout>
</template>

<style scoped>
h3 {
    width: 100%;
    margin-top: 0px;
    text-transform: capitalize;
}

.badgeGutter {
    padding-left: 8px;
    padding-right: 8px;
}

.badgeGutter:nth-of-type(3n + 1) {
    padding-left: 0px !important;
}

.badgeGutter:nth-of-type(3n) {
    padding-right: 0px !important;
}
</style>

<script lang="ts">
import { Vue, Prop, Lifecycle, Component, p } from "av-ts";
import { IBadge } from "../../interfaces/models";

import UserBadge from "../util/UserBadge.vue";
import BadgeService from "../../services/BadgeService";
import Fetcher from "../../services/Fetcher";

@Component({
    components: {
        "user-badge": UserBadge
    }
})
export default class CollectedBadges extends Vue {
    @Prop topic = p<string>({
        required: true
    });

    pAvailableBadges: IBadge[] = [];

    updateAvailableBadges(newBadges: IBadge[]) {
        this.pAvailableBadges = newBadges;
    };

    @Lifecycle
    created() {
        Fetcher.get(BadgeService.getAllUserBadges)
            .on(this.updateAvailableBadges);
        BadgeService.getAllUserBadges()
            .then(x => {
                Fetcher.get(BadgeService.getAllUserBadges)
                    .update(x);
            });
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(BadgeService.getAllUserBadges)
            .off(this.updateAvailableBadges);
    }

    get availableBadges() {
        if (this.topic == "closest") {
            return BadgeService.getClosestUserBadges(this.pAvailableBadges);
        } else if (this.topic == "all") {
            return this.pAvailableBadges;
        } else {
            return BadgeService.getBadgesByCategory(this.pAvailableBadges, this.topic);
        }
    }
}
</script>
