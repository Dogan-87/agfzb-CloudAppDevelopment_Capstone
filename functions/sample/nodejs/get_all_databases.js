const Cloudant = require('@cloudant/cloudant');

secret={
    "COUCH_URL": "https://45c14cd9-04bc-467b-a5fc-65c842636775-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "-lTAU8tc-rHV1d0JQqwjHTyD7SYClm4nPLWPG7yML22F",
    "COUCH_USERNAME": "45c14cd9-04bc-467b-a5fc-65c842636775-bluemix"
}

function main(params) {

    const cloudant = Cloudant({
        url: secret.COUCH_URL,
        plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
    });

    let dbList = getDbs(cloudant);
    return { dbs: dbList };
}

async function main(params) {
    const cloudant = Cloudant({
        url: secret.COUCH_URL,
        plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } }
    });
    try {
    let dbList = await cloudant.db.list();
    return { "dbs": dbList };
    } 
    catch (error) {
    return { error: error.description };
    }
}