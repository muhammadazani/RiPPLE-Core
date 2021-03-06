<template>
    <md-layout md-flex="100">
        <ul class="responsesContainer">
            <li v-for="(possibleAnswer, index) in question.distractors"
                :key="index"
                :class="getResponseStyles(possibleAnswer)">
                <div v-if="disabledResponses.find(x => x == possibleAnswer) || userHasCorrectAnswer"
                    class="answerOption">
                    <div class="answerIcon">
                        <md-icon>{{ optionIcon(possibleAnswer) }}</md-icon>
                    </div>
                    <span class="distractorIndex">{{distractorIndex(index)}}.</span>
                </div>
                <md-radio v-else
                    class="answerOption"
                    :disabled="!!disabledResponses.find(x => x == possibleAnswer)"
                    :md-value="index"
                    v-model="questionResponse"
                    name="answer"
                    @click.native="clickedResponse"
                    :id="'' + possibleAnswer.id">
                        <span class="distractorIndex">{{distractorIndex(index)}}.</span>
                </md-radio>
                <div class="questionContent" @click="questionResponse = index" v-html="possibleAnswer.content"></div>
                <div class="distributionOverlay"
                    :style="answerOptionFill(possibleAnswer)"></div>
            </li>
        </ul>
        <transition name="feedbackGroup"
            @enter="feedbackEnter"
            @after-enter="scrollToExplanation"
            @leave="feedbackLeave"
            :css="false">
            <md-layout md-flex="100"
                md-gutter="8"
                v-if="userHasCorrectAnswer">
                <md-layout md-flex="100"
                    class="componentSeparator"
                    md-gutter>
                    <md-card>
                        <h2>{{userHasCorrectAnswer ? "Correct" : "Incorrect"}}</h2>
                        <p v-if="userHasCorrectAnswer"><span v-html="question.explanation"></span></p>
                    </md-card>
                </md-layout>

                <md-layout
                    v-if="!preview"
                    md-flex="100"
                    md-gutter
                    class="componentSeparator">
                    <md-card class="placeBetween">
                        <question-rater icon="school"
                            :rateAction="rate('difficulty')"
                            :defaultValue="question.difficulty">Rate Difficulty</question-rater>
                        <question-rater class="ratingCard"
                            :rateAction="rate('quality')"
                            :defaultValue="question.quality">Rate Quality</question-rater>
                    </md-card>
                </md-layout>
            </md-layout>
        </transition>
    </md-layout>
</template>

<style scoped>
.distractorIndex {
    line-height: 24px;
    font-size: 14px;
    height: 24px;
    flex: 1;
    align-items: center;
    display: flex;
    margin-left: 0.5em;
}
.responsesContainer {
    list-style: none;
    margin: 0px;
    padding: 0px;
    width: 100%;
    margin-bottom: 1em;
    margin-top: 1em;
}

.responsesContainer li {
    list-style: none;
    cursor: pointer;
    position: relative;
    transition: background-color 500ms ease;
    width: 100%;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    border: 1px solid #ddd;
    margin: 0px 8px 16px 0;
}
.answerOption {
    background-color: #fafafa;
    width: 100%;
    border-bottom: 1px solid #ddd;
    border-top: 1px solid #ddd;
    padding: 1em;
    margin-top: 0px;
    margin-bottom: 0px !important;
    display: flex;
    flex: 1;
    align-items: center;
}
.answered.incorrect .answerOption {
    background-color: #f1dfdf;
}
.answered.correct .answerOption {
    background-color: #256;
}

.answerOption .answerIcon {
    margin-left: -4px;
    display: inline-block;
}

.questionContent {
    padding: 1em;
}

.distributionOverlay {
    height: 100%;
    width: 0px;
    position: absolute;
    top: 0px;
    left: 0px;
    transition: width 750ms ease;
    pointer-events: none;
}

.incorrect .distributionOverlay {
    background-color: rgba(255, 0, 0, 0.2);
}

.correct .distributionOverlay {
    background-color: rgba(34, 85, 102, 0.4);
}

h2 {
    margin: 0px;
    width: 100%;
}

.correctFill {
    background-color: rgba(34, 85, 102, 0.4) !important;
    min-width: 100%;
}

.placeBetween {
    justify-content: space-between;
}
</style>
<style>
.answerOption .md-radio-label {
    height: auto !important;
    padding-left: 0px !important;
    margin-left: 0px !important;
}

.answerOption .md-radio-container {
    min-width: 20px;
    min-height: 20px;
}
</style>

<script lang="ts">
import { Vue, Component, Lifecycle, Watch, Prop, p } from "av-ts";
import { IQuestion, IDistractor } from "../../interfaces/models";
import { addEventsToQueue } from "../../util";
import Comment from "../util/Comment.vue";
import QuestionRater from "./QuestionRater.vue";
import QuestionService from "../../services/QuestionService";
import * as d3 from "d3";

@Component({
    components: {
        QuestionRater,
        Comment
    }
})
export default class QuestionResponse extends Vue {
    @Prop question = p<IQuestion>({
        required: true
    });

    @Prop preview = p<boolean>({
        default: false
    });

    userAnswer: number = -1;
    hasGivenUp = false;
    disabledResponses: IDistractor[] = [];

    pResponseDistribution: {[id: number]: number} = {};

    updateResponseDistribution(newDistribution: {[responseId: number]: number}) {
        this.pResponseDistribution = newDistribution;
    }

    @Lifecycle
    created() {
        if (!this.preview) {
            QuestionService.distributionForQuestion(this.question)
                .then(this.updateResponseDistribution);
        }
    }

    @Watch("question")
    questionChanged(_oldQuestion: IQuestion, _newQuestion: IQuestion) {
        if (!this.preview) {
            QuestionService.distributionForQuestion(this.question)
                .then(this.updateResponseDistribution);
        }
    }

    feedbackEnter(el: HTMLElement, done: Function) {
        el.style.height = "auto";
        const actualHeight = el.clientHeight;
        el.style.height = "0px";
        d3.select(el)
            .style("overflow", "hidden")
            .style("padding-top", "0")
            .style("padding-bottom", "0")
            .transition()
            .style("height", actualHeight + "px")
            .style("opacity", 1)
            .style("margin-bottom", "1em")
            .style("padding-top", "16px")
            .style("padding-bottom", "16px")
            .duration(500)
            .on("end", () => {
                el.style.height = "auto";
                done();
            });
    }

    scrollToExplanation(el: HTMLElement) {
        el.scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
    }

    feedbackLeave(el: HTMLElement, done: Function) {
        d3.select(el)
            .transition()
            .style("height", "0px")
            .style("opacity", 0)
            .duration(500)
            .on("end", () => {
                done();
            });
    }

    getResponseStyles(answer: IDistractor) {
        const answerIcon = this.optionIcon(answer);
        return {
            answered: this.disabledResponses.find(x => x == answer) || this.userHasCorrectAnswer,
            correct: this.userHasCorrectAnswer && answerIcon == "done",
            incorrect: this.userHasCorrectAnswer && answerIcon != "done"
        };
    }

    // Getter/Setter for radio buttons
    get questionResponse() {
        return this.userAnswer;
    }

    set questionResponse(newValue: number) {
        if (this.userHasCorrectAnswer) {
            return;
        }

        const distractor = this.question.distractors[newValue];
        this.disabledResponses.push(distractor);
        this.userAnswer = newValue;

        if (!this.preview) {
            QuestionService.submitResponse({ responseId: distractor.id })
                .then(() => {
                    this.$emit("userAnswer", this.userHasCorrectAnswer);
                });
        }
    }

    answerOptionFill(response: IDistractor) {
        if (this.userHasCorrectAnswer) {
            return {
                width: this.pResponseDistribution[response.id] + "%"
            };
        }
        return {};
    }

    distractorIndex(index: number) {
        return String.fromCharCode("A".charCodeAt(0) + index);
    }

    optionIcon(solution: IDistractor) {
        return this.question.solution == solution ? "done" : "clear";
    }

    get userHasCorrectAnswer() {
        return this.question.distractors[this.questionResponse] == this.question.solution;
    }

    resetAnswer() {
        this.disabledResponses.push(this.question.distractors[this.questionResponse]);
        this.questionResponse = -1;
    }

    // Bubble event down to radio button
    clickedResponse(e: MouseEvent) {
        const target = e.target as HTMLElement;
        if (target.tagName != "LABEL" && target.tagName != "INPUT") {
            const input = target.querySelector("input");
            if (input === null) return;

            const event = new MouseEvent("click", {
                bubbles: true
            });
            input.dispatchEvent(event);
        }
    }

    rate(rateType: string) {
        if (!this.preview) {
            return (rateValue: number) => {
                QuestionService.submitRating({
                    responseId: this.question.distractors[this.userAnswer].id,
                    rateType: rateType,
                    rateValue: rateValue
                })
                .then(() => {
                    addEventsToQueue([{
                        name: "Question Rated",
                        description: "Successfully rated question " + rateType,
                        icon: "done"
                    }]);
                });
            };
        } else {
            return "";
        }
    }
}
</script>
