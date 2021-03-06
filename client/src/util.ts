import Vue from "vue";
import { ISnackbarNotification, INotification } from "./interfaces/models";

// From https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144
export function getParameterByName(name: string, url: string) {
    name = name.replace(/[\[\]]/g, "\\$&");
    let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    let results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return "";
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

const _bus = new Vue();

export const NEW_QUEUE_ITEM = "NEW_QUEUE_ITEM";

export function isAdmin(roles: string[]) {
    const adminRoles = ["Instructor", "TeachingAssistant"];
    for (let i of adminRoles) {
        if (roles.indexOf(i) >= 0) {
            return true;
        }
    }
    return false;
}

export function addEventsToQueue(items: ISnackbarNotification[]) {
    items.forEach(x => {
        _bus.$emit(NEW_QUEUE_ITEM, x);
    });
}

export function notificationToSnackbar(notification: INotification) {
    return {
        name: notification.name,
        description: notification.description,
        icon: notification.icon
    };
}

export function getBus() {
    return _bus;
}

export function serverToLocal(UTCTimestamp: number) {
    const date = new Date(0);
    date.setUTCSeconds(UTCTimestamp);

    return ("0" + date.getDate()).slice(-2) + "-" + ("0" + (date.getMonth() + 1)).slice(-2) + "-" + date.getFullYear();
}

export function localToUTC(date?: string) {
    if (date === undefined) return undefined;

    const [year, month, day] = date.split("-");
    // Convert to UTC and from milliseconds to seconds
    return Date.UTC(+year, +month, +day) / 1000;
}

export function getDefaultConsentForm() {
    return `
<h1>Consent Form</h1>
<div>
    <h2>
        <strong>
            Before you begin, we'd like to ask for your consent to collect (and de-identify) your learning and
            participation data for research into how we can improve our teaching.
        </strong>
    </h2>
    <h3>PARTICIPATION INFORMATION SHEET: </h3>
    <div>
        <p>
            <em>
                Enhancing academic and practitioner skills in first year Engineers using an
                active learning course architecture.
            </em>
        </p>
        <p>Dear student, __ seeks your participation in a project run by the course
            coordinators of __ at __. The purpose of the proposed study is to:
        </p>
        <p>
            <em>
                Ascertain whether providing authentic learning experiences (those with unstructured and integrative
                learning activities with open-ended problems) affects the coverage of core engineering technical
                concepts, and whether these experiences provide an added benefit to the development of a student's
                engineering knowledge, abilities and professional identity.
            </em>
        </p>
        <p>
            The study will be completed over the duration of __. Information gathered will be used in the design
            of authentic first year learning environments. This information will also allow a comparison to be made
            between active learning environments and traditional learning environments to see which approach is best in
            developing both engineering technical competencies, as well as professional engineering identities. We
            would be pleased if you would agree to be involved in this research.
        </p>
        <p>
            At the beginning and the end of the first year courses, you may be asked to complete short surveys during
            class time that ask for your own judgements about what you are learning/have learned in the course.
            Information on how you interact with Blackboard, online course resources, course Facebook pages, and
            question and answer and help tools will be kept on file, and may be used (anonymously only) to understand
            more about what learning processes are the most helpful to students for successful learning. Some photos or
            short videos (about 5 minutes) of team activities in workshops and in laboratory sessions may be created
            during the courses. Creation of videos and photos will only be conducted by outside researchers who have no
            influence on the course or on any student's results. Some focus group sessions may be run to ask about
            your experiences. Any collection of learning data other than what is generated by you in the online
            environment will be announced via Blackboard and you will be free to volunteer or not for these at that
            time.
        </p>
        <p>
            All information that you provide will remain completely confidential, and your name will not be linked to
            any of your data or any comments you make online or on surveys, during interviews or focus groups. Fake
            identifications will be given to your data which will be used to analyse all data that is collected.
            No identifying information from any of the data collected will be revealed to the lecturers or to the
            tutors or in the project report. All identifiable information will be kept on a secure server, owned by
            the Faculty and only accessed by authorised researchers. Only anonymous data will be accessible to the
            researchers via password protection. Confidentiality of your participation will be highly secured.
        </p>
        <p>
            You are free to choose not to participate in any of the data collection methods, and your withdrawal will
            have no bearing on your marks or on your standing in the course. You have the right to withdraw your
            permission for your information to be used at any time. If you choose to withdraw after any of the data has
            been collected, the data records which relate to you will be immediately deleted or destroyed and not used
            in the study. To withdraw from the study or any sections of the study, you need to email the data manager
            at <a href="__@__">__@__</a>. The information regarding your
            withdrawal will only be viewed by independent researchers and data management staff. For future reference,
            the Participant Information Sheet can be found under the Learning Resources tab on the course site. We
            appreciate your participation in this study. We will provide you with a summary of the information gathered
            using the above methods, if you are interested.
        </p>
        <p>
            This study has been cleared by the human ethics committees of the University of Queensland in accordance
            with the guidelines of the National Health and Medical Research Council, the Australian Human Ethics
            Committee and the Human Research Ethics Committee. You are free to discuss taking part in this study with
            the researcher (__, __). If you would like to speak to an officer of the __
            not involved in the study, you may contact the Ethics Officer on __.
        </p>
        <p> Yours sincerely, </p>
        <p> __ </p>
        <p> __ </p>
        <p> __ </p>
        <p> __ </p>
        <p> __ </p>
    </div>
    <h2><strong>Title of the Project: </strong></h2>
    <h2>
        <em>
            Project Title
        </em>
    </h2>
    <h3>Researcher Contact Details:</h3>
        <h3>__</h3>
        <h4>Email: <em>__</em></h4>
        <h4>Phone: <em>__</em> </h4>
        <h3>By clicking "I Agree", you consent to participate in this study and agree to the following:</h3>
        <ul>
            <li>
                I understand that this research project will entail surveys, activities, photos and videos of team
                activities, and data collection on my use of Blackboard and online course learning materials and help
                systems, including the course Facebook pages.
            </li>
            <li>
                I understand that any information taken will be de-identified (i.e. my personal details will not be
                used in the research), and that access to information will be limited to researchers nominated on the
                Ethics Consent Form.</li>
            <li>
                I understand that participation in the research is voluntary, and I can withdraw at any time without
                prejudice.
            </li>
            <li>
                I understand that I may choose not to answer particular questions, or have my data removed from
                particular parts of the project without being obliged to withdraw completely from the research.
            </li>
            <li>
                I understand I can request that all or some of my data to be withdrawn at any time by emailing the data
                manager at <a href="__@__">__@__</a>
            </li>
            <li>
                I am aware that the Participant Information Sheet, and the contact details for the data manager are on
                the learning resources page of the course site, for future reference.
            </li>
            <li>
                I voluntarily consent to participate in this research project.
            </li>
        </ul>
        <h5>If you do not wish to participate in this study click "I Decline".</h5>
</div>`;
}
