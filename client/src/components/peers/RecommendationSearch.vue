<template>
    <md-layout md-flex="100">
        <md-layout md-flex="100"
                   class="componentSeparator">
            <table class="table">
                <thead>
                    <tr>
                        <th>Topics</th>
                        <th v-for="role in studyRoles"
                            :key="role.id">{{ role.description }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="topic in topics"
                        :key="topic.id">
                        <td>
                            <span>{{ topic.name }}</span>
                            <div class="cellOverlay"
                                 :style="getCellWeight(topic)"></div>
                        </td>
                        <td v-for="role in studyRoles"
                            :key="role.id"
                            class="centerAlign">
                            <md-checkbox class="centerCheckbox"
                                         :disabled="checkboxIsDisabled(role.description, topic)"
                                         :value="checkbox(topic, role)"
                                         @change="checkboxChange(topic, role)"
                                         :id="`${role.id}_${topic.id}`"
                                         :name="`${role.id}_${topic.id}`"></md-checkbox>
                        </td>
                    </tr>
                </tbody>
            </table>
        </md-layout>
        <md-tabs md-fixed
                :mdNavigation="false"
                class="connect-tabs">
            <md-tab md-label="Find"
                    class="tab">
                <md-layout md-flex="100"
                           md-gutter="16">
                    <md-layout md-flex="33"
                               md-gutter
                               v-for="(recommendation, i) in recommendations"
                               :key="i">
                        <recommendation-card :user="recommendation">
                            Request
                        </recommendation-card>
                    </md-layout>
                </md-layout>
            </md-tab>
            <md-tab md-label="Review"
                    class="tab">
                <md-layout md-flex="100"
                           md-gutter="16">
                    <md-layout md-flex="33"
                               md-gutter
                               v-for="(recommendation, i) in requests"
                               :key="i">
                        <recommendation-card :user="recommendation">
                            Request
                        </recommendation-card>
                    </md-layout>
                </md-layout>
            </md-tab>
        </md-tabs>
    </md-layout>
</template>

<style>

    .connect-tabs .md-tabs-navigation-container {
        background-color: #4d656d;
    }

    .connect-tabs .md-tab-header {

        background-color: rgba(34,85,102, 0.7);
        border-bottom: 6px solid #f2f2f2;
    }

    .connect-tabs .md-tab-header:hover {
        background-color: rgba(34,85,102, 0.4);
    }

    .connect-tabs span {
        font-weight: bold;
        font-family: Verdana,Arial,Helvetica,sans-serif;
    }
    .connect-tabs .md-active span{
        color: #f2f2f2;
    }

    .connect-tabs .md-active {
        background-color: #256;
    }

    .connect-tabs .md-tab-indicator{
        background-color: #1d323a !important;
        height: 6px;
    }



</style>

<style scoped>
.tab {
    padding-left: 2px !important;
    padding-right: 2px !important;
}

.table {
    border: none;
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.table tbody td:first-child {
    position: relative;
}

.table thead tr {
    background-color: #256;
    color: #f2f2f2;
}

.table tbody tr:nth-child(even) {
    background-color: #efefef;
}

.table tr td,
.table thead tr th {
    text-align: center;
    padding: 8px 0px;
}

.cellOverlay {
    position: absolute;
    left: 0px;
    top: 5%;
    width: 0px;
    height: 90%;
    border: 1px solid transparent;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Prop, p } from "av-ts";

import { ITopic, IUserSummary, IEdge, IStudyRole, ICompareSet } from "../../interfaces/models";
import UserService from "../../services/UserService";
import Fetcher from "../../services/Fetcher";

import RecommendationCard from "./RecommendationCard.vue";

@Component({
    components: {
        RecommendationCard
    }
})
export default class RecommendationSearch extends Vue {
    @Prop
    topics = p<ITopic[]>({
        required: true
    });

    @Prop
    recommendations = p<IUserSummary[]>({
        required: true
    });

    @Prop
    requests = p<IUserSummary[]>({
        required: true
    });

    @Prop
    studyRoles = p<IStudyRole[]>({
        default: () => {
            return [];
        }
    });

    @Prop
    userRoles = p<Map<string, Map<string, boolean>>>({
        type: Map,
        default: () => {
            return new Map<string, Map<string, boolean>>();
        }
    });

    competencies = new Map();

    updateCompetencies(newCompetencies: ICompareSet) {
        this.competencies = newCompetencies.ownScores
            .reduce((carry: Map<ITopic, number>, x: IEdge) => {
                if (carry.get(x.source) === undefined) {
                    carry.set(x.source, x.competency);
                }
                return carry;
            }, new Map());
    };

    @Lifecycle
    created() {
        Fetcher.get(UserService.userCompetencies)
            .on(this.updateCompetencies);
    }

    checkbox(topic: ITopic, studyRole: IStudyRole): boolean {
        if (!this.userRoles.has(topic.name)) {
            return false;
        } else {
            const topicRoles = this.userRoles.get(topic.name);
            if (topicRoles !== undefined) {
                return topicRoles.get(studyRole.role) || false;
            }
            return false;
        }
    }

    checkboxChange(topic: ITopic, studyRole: IStudyRole) {
        this.$emit("change", topic.id, studyRole.id);
    }

    checkboxIsDisabled(sType: string, topic: ITopic) {
        if (sType == "Provide Mentorship") {
            const weight = this.competencies.get(topic);
            return weight === undefined || weight <= 85;
        }

        return false;
    }

    getColour(c: number) {
        if (c < 50) {
            return "rgba(255, 99, 132, ";
        } else if (c >= 50 && c < 85) {
            return "rgba(255, 206, 86, ";
        } else if (c >= 85) {
            return "rgba(34, 85, 102, ";
        }
    };

    getCellWeight(topic: ITopic) {
        const weight = this.competencies.get(topic);
        return {
            background: `${this.getColour(weight)}${0.4})`,
            borderColor: `${this.getColour(weight)}1)`,
            width: `${weight}%`
        };
    }
}
</script>
