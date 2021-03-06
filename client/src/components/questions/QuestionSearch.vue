<template>
    <md-layout md-flex="100"
               class="header" v-if="search">
        <md-layout v-for="field in searchableFields"
                   :key="field.displayName"
                   :class="searchItemClass">
            <md-input-container v-if="field.type == 'multiselect'">
                <label :for="field.name">{{field.name}}</label>
                <md-select :name="field.name" multiple v-model="search[field.id]">
                    <md-option v-for="option in field.options"
                        :key="option.value"
                        :value="option.value">{{ option.name }} </md-option>
                </md-select>
            </md-input-container>
            <md-input-container v-else-if="field.type == 'select'">
                <label :for="field.name">{{field.name}}</label>
                <md-select :name="field.name"
                           :id="field.name"
                           v-model="search[field.id]">
                    <md-option v-for="option in field.options"
                               :key="option.value"
                               :value="option.value">{{ option.name }}</md-option>
                </md-select>
                <h3 v-if="field.sort && search[field.id] != ''"
                    @click="sort"
                    class="sortBy">{{ search.sortDesc ? "Descending" : "Ascending"}}
                    <md-icon :class="{rotate: search.sortDesc}">arrow_upward</md-icon>
                </h3>
            </md-input-container>

            <md-input-container v-else-if="field.type == 'text'">
                <label>{{field.name}}</label>
                <md-input class="searchField"
                          v-model="search[field.id]"></md-input>
            </md-input-container>
        </md-layout>
        <slot></slot>
        <page-loader :condition="false"></page-loader>
    </md-layout>
</template>

<style scoped>
.rotate {
    transform: rotate(-180deg);
}

.header {
    justify-content: space-between;
    width: 100%;
    flex-wrap: nowrap;
    position: relative;
    min-width: 800px;
}

.searchItem:first-of-type {
    margin-left: 0px;
}
.searchItem:last-of-type {
    margin-right: 0px;
}

.searchItem {
    overflow: hidden;
    margin-left: 20px;
    margin-right: 20px;
}

.mobileSearchItem {
    overflow: hidden;
    margin-left: 0px;
    margin-right: 15px;
}

h2 {
    color: #999;
}

.sortBy {
    cursor: pointer;
    display: inline-flex;
    margin-left: 25px;
    align-items: center;
    color: rgba(0, 0, 0, 0.54);
    font-size: 16px;
    font-weight: 400;
}

.sortBy>i {
    font-size: 16px;
    padding-left: 6px;
    cursor: pointer;
    transition: 250ms ease transform;
}

h3 {
    user-select: none;
    margin: 0px 10px 0px 0px;
}

input {
    width: 150px;
    height: 25px;
    display: inline-block;
    vertical-align: middle;
}

.searchField {
    font-size: 16px !important;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Watch, Prop, p, Mixin as mixin } from "av-ts";
import { ITopic, ISearch } from "../../interfaces/models";

import QuestionService from "../../services/QuestionService";
import TopicService from "../../services/TopicService";
import Fetcher from "../../services/Fetcher";
import responsiveMixin from "../../responsiveMixin";
import PageLoader from "../util/PageLoader.vue";

@Component({
    components: {
        PageLoader
    }
})
export default class QuestionSearch extends mixin(responsiveMixin, Vue) {

    timeoutId: number | undefined = undefined;
    nextSearchRequest: Function| undefined = undefined;

    @Prop
    page = p<number>({
        default: 1
    });
    @Prop
    pageSize = p<number>({
        default: 25
    });

    pTopics: ITopic[] = [];

    get searchableFields() {
        return [{
            name: "Sort By",
            id: "sortField",
            type: "select",
            sort: true,
            options: [{
                name: "",
                value: ""
            }, {
                name: "Recommended",
                value: "recommended"
            }, {
                name: "Difficulty",
                value: "difficulty"
            }, {
                name: "Quality",
                value: "quality"
            }, {
                name: "Created Time",
                value: "created_time"
            }, {
                name: "Responses",
                value: "responses"
            }]
        }, {
            name: "Filter Topics",
            id: "filterTopics",
            type: "multiselect",
            options: this.topics.map(topic => ({
                name: topic.name,
                value: topic.id
            }))
        }, {
            name: "Filter Questions",
            id: "filterField",
            type: "select",
            options: [{
                name: "All Questions",
                value: ""
            }, {
                name: "Unanswered Questions",
                value: "unanswered"
            }, {
                name: "Answered Questions",
                value: "answered"
            }/*, {
                name: "Room for Improvement",
                value: "improve"
            }*/]
        }, {
            name: "Search",
            id: "query",
            type: "text"
        }];
    }

    search: ISearch | undefined = undefined;

    updateCourseTopics(newTopics: ITopic[]) {
        this.pTopics = newTopics;
        QuestionService.getSearchCacheForCourse()
            .then(x => {
                this.search = x;
            });
    }

    get topics() {
        return this.pTopics;
    }

    @Lifecycle
    created() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .on(this.updateCourseTopics);
    }

    @Lifecycle
    destroyed() {
        Fetcher.get(TopicService.getAllAvailableTopics)
            .off(this.updateCourseTopics);
    }

    sort() {
        if (this.search !== undefined) {
            this.search.sortDesc = !this.search.sortDesc;
        }
    }

    applyFilters() {
        const search = Object.assign({}, this.search, { page: this.page, pageSize: this.pageSize });
        if (search.filterTopics.length == 0) {
            search.filterTopics = this.topics.map(x => x.id);
        }
        QuestionService.search(search)
            .then(searchResult => {
                this.timeoutId = undefined;
                if (this.nextSearchRequest != undefined) {
                    this.nextSearchRequest();
                    this.nextSearchRequest = undefined;
                } else {
                    if (this.search !== undefined) {
                        QuestionService.setSearchCacheForCourse(this.search);
                    }
                    // Only bubble through the most recent search
                    this.$emit("searched", searchResult);
                }
            });
    }

    @Watch("page")
    pageChanged(_newVal: number, _oldVal: number) {
        this.startSearch();
    }

    @Watch("pageSize")
    pageSizeChanged(_newVal: number, _oldVal: number) {
        this.startSearch();
    }

    @Watch("search", { deep: true })
    searchWatch(_oldValue: ISearch | undefined, _newValue: ISearch| undefined) {
        this.startSearch();
    }

    startSearch() {
        if (this.timeoutId === undefined) {
            this.timeoutId = window.setTimeout((() => this.applyFilters()), 10);
        } else {
            this.nextSearchRequest = () => {
                this.timeoutId = window.setTimeout((() => this.applyFilters()), 10);
            };
        }
    }

    get searchItemClass() {
        return {
            "searchItem": !this.mobileMode,
            "mobileSearchItem": this.mobileMode
        };
    }

}
</script>
