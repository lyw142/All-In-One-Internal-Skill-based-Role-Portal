import { createApp } from "vue";
import { mount } from "@vue/test-utils";
import Candidates from "./Candidates.vue";
import Cookies from "js-cookie";
import axios from "axios";
import { setupServer } from "msw/node";
import { rest } from "msw";
import { test } from "vitest";

import { JSDOM } from "jsdom";

const { window } = new JSDOM("<body></body>");
global.document = window.document;
global.window = window;

const server = setupServer(
  rest.get("http://127.0.0.1:5000/api/getapplications", (req, res, ctx) => {
    return res(ctx.json([])); // returns an empty array
  }),
  rest.get(
    "http://127.0.0.1:5000/api/getRoleListing/:listingId",
    (req, res, ctx) => {
      return res(ctx.json([])); // returns an empty array
    }
  ),
  rest.get(
    "http://127.0.0.1:5000/api/getApplicantsBySkillMatch/:listingId",
    (req, res, ctx) => {
      return res(ctx.json([])); // returns an empty array
    }
  ),
  rest.get("http://127.0.0.1:5000/api/skills", (req, res, ctx) => {
    return res(ctx.json([])); // returns an empty array
  })
);

const setup = () => {
  server.listen();
};

const reset = () => {
  server.resetHandlers();
};

const tearDown = () => {
  server.close();
};

const runTest = async (callback) => {
  setup();
  await callback();
  reset();
  tearDown();
};

test("Candidates.vue", () => {
  // All your test cases go here
  test("fetchApplications", async () => {
    server.use(
      rest.get("http://127.0.0.1:5000/api/getapplications", (req, res, ctx) => {
        return res(
          ctx.json([
            {
              Staff_ID: 1,
              Listing_ID: 1,
              Role_Name: "Software Engineer",
            },
          ])
        );
      })
    );

    const wrapper = mount(Candidates);

    await wrapper.vm.fetchApplications();

    expect(wrapper.vm.$data.applications).toHaveLength(1);

    expect(wrapper.vm.$data.roles).toHaveLength(1);
  });

  test("fetchRoleListing", async () => {
    server.use(
      rest.get(
        "http://127.0.0.1:5000/api/getRoleListing/:listingId",
        (req, res, ctx) => {
          return res(
            ctx.json([
              {
                Listing_ID: 1,
                Role_Name: "Software Engineer",
              },
            ])
          );
        }
      )
    );

    const wrapper = mount(Candidates);

    await wrapper.vm.fetchRoleListing(1);

    expect(wrapper.vm.$data.applications[0].roleListing).toBeTruthy();
  });

  test("countApplications", () => {
    const wrapper = mount(Candidates);

    wrapper.setData({
      applications: [
        {
          Listing_ID: 1,
          Role_Name: "Software Engineer",
        },
      ],
      selectedRole: {
        Listing_ID: 1,
        Role_Name: "Software Engineer",
      },
    });

    wrapper.vm.countApplications();

    expect(wrapper.vm.$data.applicationCount).toBe(1);
  });

  test("getApplicantBySkillCount", async () => {
    server.use(
      rest.get(
        "http://127.0.0.1:5000/api/getApplicantsBySkillMatch/:listingId",
        (req, res, ctx) => {
          return res(
            ctx.json([
              {
                Staff_ID: 1,
                Listing_ID: 1,
              },
            ])
          );
        }
      )
    );

    const wrapper = mount(Candidates);

    await wrapper.vm.getApplicantBySkillCount();

    expect(wrapper.vm.$data.applicationsforCount).toHaveLength(1);
  });

  test("showTable", () => {
    const wrapper = mount(Candidates);

    wrapper.vm.showTable();

    expect(wrapper.vm.$data.sortOrder).toBe(false);

    expect(wrapper.vm.$data.sortCount).toBe(true);
  });

  test("fetchSkills", async () => {
    server.use(
      rest.get("http://127.0.0.1:5000/api/skills", (req, res, ctx) => {
        return res(
          ctx.json([
            {
              Skill_ID: 1,
              Skill_Name: "Vue.js",
            },
          ])
        );
      })
    );

    const wrapper = mount(Candidates);

    await wrapper.vm.fetchSkills();

    expect(wrapper.vm.$data.availableSkills).toHaveLength(1);
  });

  test("openModal", () => {
    const wrapper = mount(Candidates);

    wrapper.vm.openModal({
      Staff_ID: 1,
      Staff_FName: "John",
      Staff_LName: "Doe",
    });

    expect(wrapper.vm.$data.selectedCandidate).toBeTruthy();
  });

  test("closeModal", () => {
    const wrapper = mount(Candidates);

    wrapper.vm.openModal({
      Staff_ID: 1,
      Staff_FName: "John",
      Staff_LName: "Doe",
    });

    wrapper.vm.closeModal();

    expect(wrapper.vm.$data.selectedCandidate).toBeNull();
  });

  test("sortedCandidates", () => {
    const wrapper = mount(Candidates);

    wrapper.setData({
      applications: [
        { Application_Date: new Date(2022, 1, 1), Listing_ID: 1 },
        { Application_Date: new Date(2021, 1, 1), Listing_ID: 1 },
      ],
      selectedRole: {
        Listing_ID: 1,
        Role_Name: "Software Engineer",
      },
    });

    expect(wrapper.vm.sortedCandidates[0].Application_Date).toBe(
      new Date(2021, 1, 1)
    );
  });

  test("filteredCandidates", () => {
    const wrapper = mount(Candidates);

    wrapper.setData({
      rolecandidates: [
        { Skills: [{ Skill_Name: "Vue.js" }, { Skill_Name: "JavaScript" }] },
        { Skills: [{ Skill_Name: "Vue.js" }, { Skill_Name: "Python" }] },
      ],
      selectedSkills: ["Vue.js", "JavaScript"],
    });

    expect(wrapper.vm.filteredCandidates).toHaveLength(1);
  });
});
